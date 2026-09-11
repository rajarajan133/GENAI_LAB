import chromadb
from chromadb.utils import embedding_functions

# 1. Create a local persistent Chroma database
client = chromadb.PersistentClient(path="./.chroma")

# 2. Use the local Sentence Transformer model
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 3. Create/get our knowledge-base collection
col = client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=embed_fn
)

# 4. Add documents
col.add(
    ids=["a", "b", "c"],
    documents=[
        "You can cancel your subscription from Settings → Billing.",
        "Refunds are issued within 7 business days.",
        "Two-factor authentication uses TOTP apps.",
    ],
)

# 5. Search using natural language
query = "how do I stop being charged?"

hits = col.query(
    query_texts=[query],
    n_results=2
)

# 6. Display results
print(f"\nQuery: {query}\n")
print("Most relevant documents:\n")

for doc, dist in zip(
    hits["documents"][0],
    hits["distances"][0]
):
    print(f"Distance: {dist:.3f}")
    print(f"Document: {doc}")
    print()
