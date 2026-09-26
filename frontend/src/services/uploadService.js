import api from "./api";

export async function uploadPDF(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/api/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function getDocuments() {
  const response = await api.get("/api/upload/documents");
  return response.data;
}

export async function deleteDocument(documentId) {
  const response = await api.delete(
    `/api/upload/documents/${encodeURIComponent(documentId)}`
  );
  return response.data;
}