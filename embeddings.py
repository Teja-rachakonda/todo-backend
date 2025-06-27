from sentence_transformers import SentenceTransformer
from langsmith import traceable  # ✅ LangSmith manual tracing

embedding_model = SentenceTransformer("all-mpnet-base-v2")

@traceable(name="Generate Embedding")
def embed(text: str) -> list:
    """Return embeddings for given text."""
    return embedding_model.encode(text).tolist()
