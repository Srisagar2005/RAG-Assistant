import api from "./api";

export async function askQuestion(question) {
  const response = await api.post("/api/query/", { question });
  return response.data;
}
