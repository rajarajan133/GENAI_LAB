import chromadb
from chromadb.utils import embedding_functions
import ollama


# 1. Local ChromaDB
chroma_client = chromadb.PersistentClient(path="./.chroma")


# 2. Local embedding model
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


# 3. Knowledge base
col = chroma_client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=embed_fn
)


# 4. Add test documents
col.upsert(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "You can cancel your subscription from Settings → Billing.",
        "Refunds are issued within 7 business days.",
        "Two-factor authentication uses TOTP authenticator applications."
    ]
)


# 5. RAG system prompt
SYSTEM = """You are a document question-answering assistant.

Answer ONLY using the provided evidence.

Do not use your own knowledge.
Do not add greetings, introductions, or unrelated text.

If the evidence does not contain enough information to answer the question,
say: "The provided evidence does not contain enough information to answer this question."

Every factual claim must include its source citation in this format:
[#0], [#1], etc.

Return only the answer."""

# 6. RAG function
def answer(question: str) -> str:

    # Retrieve relevant documents
    hits = col.query(
        query_texts=[question],
        n_results=4
    )

    # Build evidence
    evidence = "\n\n".join(
        f"[#{i}] {doc}"
        for i, doc in enumerate(hits["documents"][0])
    )

    # Send evidence to local Llama 3.2
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": SYSTEM
            },
            {
                "role": "user",
                "content": f"""Evidence:

{evidence}

Question:

{question}
"""
            }
        ],
        options={
            "temperature": 0.1
        }
    )

    return response["message"]["content"]


# 7. Test question
question = "How do I stop being charged?"

print("\n==============================")
print("QUESTION:")
print(question)

print("\nRAG ANSWER:")
print(answer(question))
print("==============================")
