"""
Retrieval quality metrics: Precision@k and Mean Reciprocal Rank (MRR).

These are pure functions — they take retrieved chunk IDs and a set of
ground-truth relevant chunk IDs, nothing else. They don't know about
Chroma, reranking, or the app at all, which makes them independently
testable with dummy data before any real eval set exists.

A "chunk ID" here is a (filename, chunk_index) pair, identified via
chunk_id() below. Using the display filename + chunk index (rather
than the internal UUID-prefixed document_id) is a deliberate choice:
it's what a human labeling the eval set can read and reason about
directly off the retrieved sources. The tradeoff is that if the same
filename gets uploaded twice (two different document_ids), a chunk_id
could theoretically collide — an accepted limitation for a small,
manually curated eval set.
"""


def chunk_id(filename: str, chunk_index: int) -> str:
    return f"{filename}::{chunk_index}"


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    """
    Precision@k = (# relevant chunks in the top-k retrieved) / k

    retrieved_ids: chunk IDs in the order they were retrieved/ranked
                   (best first).
    relevant_ids:  ground-truth set of chunk IDs considered relevant
                   for this question.
    """
    if k <= 0:
        return 0.0

    top_k = retrieved_ids[:k]
    hits = sum(1 for cid in top_k if cid in relevant_ids)

    return hits / k


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    """
    Reciprocal Rank = 1 / (1-indexed rank of the first relevant chunk).
    Returns 0.0 if no relevant chunk appears anywhere in retrieved_ids.
    """
    for rank, cid in enumerate(retrieved_ids, start=1):
        if cid in relevant_ids:
            return 1.0 / rank

    return 0.0


def mean_precision_at_k(
    list_of_retrieved_ids: list[list[str]],
    list_of_relevant_ids: list[set[str]],
    k: int,
) -> float:
    """
    Average Precision@k across a set of questions.
    """
    if not list_of_retrieved_ids:
        return 0.0

    scores = [
        precision_at_k(retrieved, relevant, k)
        for retrieved, relevant in zip(list_of_retrieved_ids, list_of_relevant_ids)
    ]

    return sum(scores) / len(scores)


def mean_reciprocal_rank(
    list_of_retrieved_ids: list[list[str]],
    list_of_relevant_ids: list[set[str]],
) -> float:
    """
    MRR = average Reciprocal Rank across a set of questions.
    """
    if not list_of_retrieved_ids:
        return 0.0

    scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(list_of_retrieved_ids, list_of_relevant_ids)
    ]

    return sum(scores) / len(scores)
