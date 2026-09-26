from pydantic import BaseModel


class Source(BaseModel):
    filename: str
    chunk_index: int
    distance: float


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]