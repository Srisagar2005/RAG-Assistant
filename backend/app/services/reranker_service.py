"""
Cross-encoder reranking.

Embedding-distance retrieval (bi-encoder) scores the query and each
document independently, then compares vectors — fast, but it can miss
relevance nuances. A cross-encoder scores the query and document
*together* in one forward pass, which is slower but more accurate.
Here it's used as a second pass: Chroma returns a wider candidate pool
by embedding distance, then the cross-encoder re-scores and re-orders
just that pool down to top_k.

Runs locally (no external API), toggleable via RERANK_ENABLED so its
effect on latency/quality can be measured with it on vs. off.
"""

from sentence_transformers import CrossEncoder

_RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_model = None


def _get_model() -> CrossEncoder:
    global _model
    if _model is None:
        _model = CrossEncoder(_RERANK_MODEL_NAME)
    return _model


def rerank_candidates(query: str, candidates: list[dict], top_k: int) -> list[dict]:
    """
    Re-score and re-order retrieved candidates using a cross-encoder.

    Each candidate dict must have a "document" key; this adds a
    "rerank_score" key (higher = more relevant) and returns the
    top_k candidates sorted by that score, descending.

    If the reranker fails to load or run for any reason, this falls
    back to the original (embedding-distance) order — reranking is a
    quality enhancement, not something a query should hard-fail on.
    """
    if not candidates:
        return candidates

    try:
        model = _get_model()
        pairs = [(query, c["document"]) for c in candidates]
        scores = model.predict(pairs)
    except Exception as e:
        print(f"Reranking failed, falling back to embedding-distance order: {e}")
        return candidates[:top_k]

    for candidate, score in zip(candidates, scores):
        candidate["rerank_score"] = float(score)

    candidates.sort(key=lambda c: c["rerank_score"], reverse=True)

    return candidates[:top_k]
