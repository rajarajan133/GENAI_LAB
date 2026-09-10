import numpy as np
from sentence_transformers import SentenceTransformer

# Load a small embedding model locally
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> np.ndarray:
    return model.encode(text, normalize_embeddings=False)


def cosine(a, b):
    return float(
        a @ b / (np.linalg.norm(a) * np.linalg.norm(b))
    )


q = embed("How do I cancel my subscription?")

docs = [
    "Refund policy",
    "Deleting your account",
    "Kubernetes networking",
]

for doc in docs:
    score = cosine(q, embed(doc))
    print(f"{score:.3f}  {doc}")
