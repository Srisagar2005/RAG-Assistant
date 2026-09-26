import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.services.pdf_extractor import extract_text, PDFExtractionError
from app.services.text_chunker import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.chroma_service import (
    store_embeddings,
    list_documents as _list_chroma_documents,
    delete_document_chunks,
)
from app.core.metrics import metrics

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Only allow letters, numbers, dots, dashes, and underscores in the
# *display* filename we keep. Everything else gets stripped so a
# crafted filename like "../../etc/passwd.pdf" can never escape
# UPLOAD_DIR or collide with another user's file.
_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._-]")


def sanitize_filename(raw_filename: str) -> str:
    """
    Reduce an untrusted uploaded filename to a safe display name:
    - drop any directory components (path traversal)
    - strip characters outside a known-safe set
    - fall back to a generic name if nothing usable remains
    """
    name = Path(raw_filename or "").name  # strips any path components
    name = _SAFE_CHARS.sub("_", name)
    name = name.strip("._") or "document.pdf"

    if not name.lower().endswith(".pdf"):
        name += ".pdf"

    return name


def _chunk_embed_and_store(extracted_text: str, document_id: str, display_filename: str):
    """
    Synchronous, CPU-bound pipeline: chunk the text, embed the chunks,
    and persist them to Chroma. Intended to run inside a worker thread
    via run_in_threadpool so it never blocks the event loop.
    """
    chunks = chunk_text(extracted_text)
    embeddings = generate_embeddings(chunks)
    store_embeddings(chunks, embeddings, document_id, display_filename)
    return chunks, embeddings


async def save_pdf(file: UploadFile):
    safe_display_name = sanitize_filename(file.filename)

    # Prefix with a UUID so two uploads (same user or different users)
    # can never collide or overwrite each other on disk or in Chroma.
    disk_filename = f"{uuid.uuid4().hex}_{safe_display_name}"
    file_path = UPLOAD_DIR / disk_filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        extracted_text = await run_in_threadpool(extract_text, file_path)
    except PDFExtractionError as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=f"That PDF couldn't be read (it may be corrupt or password-protected): {e}"
        )

    if not extracted_text.strip():
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail="No extractable text was found in this PDF. Scanned/image-only "
                   "PDFs aren't supported yet — try a text-based PDF."
        )

    try:
        chunks, embeddings = await run_in_threadpool(
            _chunk_embed_and_store, extracted_text, disk_filename, safe_display_name
        )
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document into the vector store: {e}"
        )

    metrics.record_document_indexed()

    return {
        "filename": safe_display_name,
        "document_id": disk_filename,
        "size": file.size,
        "characters": len(extracted_text),
        "chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "stored_chunks": len(chunks),
        "status": "Document processed successfully"
    }


async def list_uploaded_documents():
    """
    Return all uploaded documents currently indexed in Chroma.
    """
    return await run_in_threadpool(_list_chroma_documents)


async def delete_document(document_id: str):
    """
    Remove a document's chunks from Chroma and its file from disk.
    """
    # document_id must be one of our own generated ids — never let a
    # crafted value walk the filesystem or query with attacker-chosen data.
    if not re.fullmatch(r"[A-Za-z0-9._-]+", document_id or ""):
        raise HTTPException(status_code=400, detail="Invalid document id.")

    deleted_count = await run_in_threadpool(delete_document_chunks, document_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = UPLOAD_DIR / document_id
    file_path.unlink(missing_ok=True)

    metrics.record_document_deleted()

    return {
        "document_id": document_id,
        "deleted_chunks": deleted_count,
        "status": "Document deleted successfully"
    }