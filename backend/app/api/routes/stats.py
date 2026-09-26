from fastapi import APIRouter

from app.core.metrics import metrics

router = APIRouter()


@router.get("/")
async def get_stats():
    """
    Returns a snapshot of in-process metrics: request/error counts,
    document indexing/deletion totals, and query pipeline latency +
    retrieval-distance stats averaged over the most recent queries.
    """
    return metrics.snapshot()
