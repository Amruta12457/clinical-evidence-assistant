import os
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder

load_dotenv()

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")


def rerank(question, chunks):
    pairs = [
        (question, chunk["content"]["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    reranked_chunks = []

    for chunk, score in zip(chunks, scores):
        reranked_chunks.append({
            "chunk": chunk,
            "rerank_score": float(score)
        })

    reranked_chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_chunks


def get_top_chunks(question, chunks, k=10):
    reranked_chunks = rerank(question, chunks)

    return [
        item["chunk"]
        for item in reranked_chunks[:k]
    ]


if __name__ == "__main__":
    from bedrock import retrieve_chunks

    question = "What were the enrollment numbers for SOLO 1 and SOLO 2?"

    chunks = retrieve_chunks(question)

    reranked_chunks = rerank(question, chunks)

    for i, result in enumerate(reranked_chunks, start=1):
        print(f"\n--- Reranked Result {i} ---")
        print("Rerank Score:", result["rerank_score"])
        print("Original Bedrock Score:", result["chunk"].get("score"))
        print("Text:", result["chunk"]["content"]["text"])