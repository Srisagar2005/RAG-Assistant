import { useState } from "react";
import { FileText, Loader2, Trash2 } from "lucide-react";
import { useDocuments } from "../../hooks/useDocuments";
import { deleteDocument } from "../../services/uploadService";

function DocumentList() {
  const { documents, loading, error, refreshDocuments } = useDocuments();
  const [deletingId, setDeletingId] = useState(null);

  const handleDelete = async (documentId) => {
    setDeletingId(documentId);

    try {
      await deleteDocument(documentId);
      await refreshDocuments();
    } catch (err) {
      console.error("Failed to delete document:", err);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="mt-6">
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-400">
        Uploaded Documents
      </h2>

      {loading ? (
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <Loader2 size={16} className="animate-spin" />
          Loading documents...
        </div>
      ) : error ? (
        <p className="text-sm text-red-400">{error}</p>
      ) : documents.length === 0 ? (
        <div className="rounded-xl border border-slate-700 bg-slate-800/40 p-4">
          <div className="flex items-center gap-3 text-slate-400">
            <FileText size={18} />
            <span>No documents uploaded</span>
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {documents.map((doc) => (
            <div
              key={doc.document_id}
              className="flex items-center justify-between gap-3 rounded-xl border border-slate-700 bg-slate-800/40 p-3"
            >
              <div className="flex min-w-0 items-center gap-2">
                <FileText size={16} className="shrink-0 text-blue-400" />
                <span
                  className="truncate text-sm text-slate-200"
                  title={doc.filename}
                >
                  {doc.filename}
                </span>
              </div>

              <button
                onClick={() => handleDelete(doc.document_id)}
                disabled={deletingId === doc.document_id}
                className="text-slate-500 transition hover:text-red-400 disabled:opacity-50"
                title="Delete document"
              >
                {deletingId === doc.document_id ? (
                  <Loader2 size={16} className="animate-spin" />
                ) : (
                  <Trash2 size={16} />
                )}
              </button>
            </div>
          ))}
        </div>
      )}

      <p className="mt-4 text-xs text-slate-500">
        {documents.length} document{documents.length === 1 ? "" : "s"} indexed
      </p>
    </div>
  );
}

export default DocumentList;