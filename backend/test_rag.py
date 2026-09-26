from app.services.rag_service import answer_question

question = "What is this document about?"

response = answer_question(question)

print("\nQuestion:\n")
print(response["question"])

print("\nAnswer:\n")
print(response["answer"])

print("\nSources:\n")

for source in response["sources"]:
    print(source)