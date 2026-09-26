from sentence_transformers import SentenceTransformer

# Load embedding model (downloads only once)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Convert text chunks into vector embeddings.
    """
    embeddings = model.encode(chunks, convert_to_numpy=True)

    return embeddings

def generate_query_embedding(query):
    """
    Generate embedding for a user's question.
    """
    return model.encode(query, convert_to_numpy=True)