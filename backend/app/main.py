from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.upload import router as upload_router
from app.api.routes.query import router as query_router
from app.api.routes.stats import router as stats_router
from app.core.metrics import metrics

app = FastAPI(
    title="Enterprise RAG Assistant",
    version="1.0.0",
    description="A production-ready RAG application built with FastAPI."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def record_request_metrics(request: Request, call_next):
    response = await call_next(request)
    metrics.record_request(response.status_code)
    return response


@app.get("/")
async def root():
    return {
        "message": "Enterprise RAG Assistant API is running 🚀"
    }


app.include_router(
    upload_router,
    prefix="/api/upload",
    tags=["Upload"]
)

app.include_router(
    query_router,
    prefix="/api/query",
    tags=["Query"]
)

app.include_router(
    stats_router,
    prefix="/api/stats",
    tags=["Stats"]
)