from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from app.schemas.query import QueryRequest
from app.services.rag_service import answer_question
from app.schemas.response import QueryResponse

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_document(request: QueryRequest):

    response = await run_in_threadpool(answer_question, request.question)

    return response