import chromadb

# Persistent database (stored on disk)
client = chromadb.PersistentClient(path="chroma_db")

# Create or load collection
collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(chunks, embeddings, document_id, display_filename):
    """
    Store document chunks and their embeddings in ChromaDB.

    document_id is the unique on-disk filename (safe to use as a
    stable key); display_filename is the human-readable name shown
    in the UI and in cited sources.
    """

    ids = []
    metadatas = []

    for i in range(len(chunks)):
        ids.append(f"{document_id}_{i}")

        metadatas.append({
            "document_id": document_id,
            "filename": display_filename,
            "chunk_index": i
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def search_similar_chunks(query_embedding, top_k=3):
    """
    Retrieve the most similar document chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results


def list_documents():
    """
    Return one entry per uploaded document (deduplicated across its
    chunks), with document_id, display filename, and chunk count.
    """
    data = collection.get(include=["metadatas"])
    metadatas = data.get("metadatas", []) or []

    docs = {}
    for meta in metadatas:
        doc_id = meta.get("document_id")
        if not doc_id:
            continue

        if doc_id not in docs:
            docs[doc_id] = {
                "document_id": doc_id,
                "filename": meta.get("filename", doc_id),
                "chunk_count": 0
            }

        docs[doc_id]["chunk_count"] += 1

    return list(docs.values())


def delete_document_chunks(document_id: str) -> int:
    """
    Delete every chunk belonging to a document. Returns how many
    chunks were deleted (0 if the document_id wasn't found).
    """
    existing = collection.get(where={"document_id": document_id}, include=[])
    existing_ids = existing.get("ids", [])

    if not existing_ids:
        return 0

    collection.delete(ids=existing_ids)
    return len(existing_ids)