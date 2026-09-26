from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import save_pdf, list_uploaded_documents, delete_document

router = APIRouter()


@router.get("/")
async def upload_home():
    return {"message": "Upload API is working!"}


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    return await save_pdf(file)


@router.get("/documents")
async def get_documents():
    return await list_uploaded_documents()


@router.delete("/documents/{document_id}")
async def remove_document(document_id: str):
    return await delete_document(document_id)