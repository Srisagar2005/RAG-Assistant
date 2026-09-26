from app.services.llm_service import LLMService

llm = LLMService()

prompt = """
Explain Retrieval-Augmented Generation (RAG) in one sentence.
"""

response = llm.generate_response(prompt)

print("\n===== LLM Response =====\n")
print(response)