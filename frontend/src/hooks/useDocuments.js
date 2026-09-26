import { useContext } from "react";
import { DocumentsContext } from "../context/documents-context-value";

export function useDocuments() {
  const context = useContext(DocumentsContext);

  if (!context) {
    throw new Error("useDocuments must be used within a DocumentsProvider");
  }

  return context;
}
