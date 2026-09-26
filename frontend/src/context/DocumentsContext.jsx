import { useEffect, useState, useCallback } from "react";
import { getDocuments } from "../services/uploadService";
import { DocumentsContext } from "./documents-context-value";

export function DocumentsProvider({ children }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const refreshDocuments = useCallback(async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
      setError(null);
    } catch (err) {
      setError("Couldn't load documents. Is the backend running?");
      console.error("Failed to fetch documents:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Standard fetch-on-mount pattern: refreshDocuments only calls
    // setState after its internal `await`, never synchronously in
    // this effect's call stack, so there's no cascading-render risk
    // here — this is the documented "synchronize with an external
    // system" use case the rule itself describes.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    refreshDocuments();
  }, [refreshDocuments]);

  return (
    <DocumentsContext.Provider
      value={{ documents, loading, error, refreshDocuments }}
    >
      {children}
    </DocumentsContext.Provider>
  );
}
