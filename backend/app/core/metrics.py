"""
Minimal in-memory metrics store.

Deliberately dependency-free (no Prometheus, no external time-series
DB) — this is scoped for a single-process demo/resume project, not a
production deployment. Metrics reset on restart and won't aggregate
correctly across multiple worker processes; a real deployment would
swap this for something like Prometheus, but that's out of scope here.
"""

import time
from collections import deque
from statistics import mean
from threading import Lock


class MetricsStore:
    def __init__(self, max_history: int = 200):
        self._lock = Lock()

        self.requests_total = 0
        self.errors_by_status = {}  # status_code -> count

        self.documents_indexed_total = 0
        self.documents_deleted_total = 0

        self.queries_total = 0
        self._query_history = deque(maxlen=max_history)

    def record_request(self, status_code: int):
        with self._lock:
            self.requests_total += 1
            if status_code >= 400:
                self.errors_by_status[status_code] = (
                    self.errors_by_status.get(status_code, 0) + 1
                )

    def record_document_indexed(self):
        with self._lock:
            self.documents_indexed_total += 1

    def record_document_deleted(self):
        with self._lock:
            self.documents_deleted_total += 1

    def record_query(self, embed_ms, retrieval_ms, generation_ms, total_ms, distances, rerank_ms=None):
        with self._lock:
            self.queries_total += 1
            self._query_history.append({
                "embed_ms": round(embed_ms, 2),
                "retrieval_ms": round(retrieval_ms, 2),
                "rerank_ms": round(rerank_ms, 2) if rerank_ms is not None else None,
                "generation_ms": round(generation_ms, 2),
                "total_ms": round(total_ms, 2),
                "avg_distance": round(mean(distances), 4) if distances else None,
                "min_distance": round(min(distances), 4) if distances else None,
                "max_distance": round(max(distances), 4) if distances else None,
            })

    def snapshot(self):
        with self._lock:
            history = list(self._query_history)
            errors_by_status = dict(self.errors_by_status)
            totals = {
                "requests_total": self.requests_total,
                "errors_by_status": errors_by_status,
                "documents_indexed_total": self.documents_indexed_total,
                "documents_deleted_total": self.documents_deleted_total,
                "queries_total": self.queries_total,
            }

        def avg(key):
            values = [h[key] for h in history if h[key] is not None]
            return round(mean(values), 2) if values else None

        return {
            **totals,
            "recent_queries_sampled": len(history),
            "avg_embed_ms": avg("embed_ms"),
            "avg_retrieval_ms": avg("retrieval_ms"),
            "avg_rerank_ms": avg("rerank_ms"),
            "avg_generation_ms": avg("generation_ms"),
            "avg_total_ms": avg("total_ms"),
            "avg_distance": avg("avg_distance"),
            "recent_queries": history[-10:],
        }


# Single process-wide instance, imported wherever a metric needs recording.
metrics = MetricsStore()
