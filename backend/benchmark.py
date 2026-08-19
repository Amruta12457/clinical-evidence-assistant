from bedrock import retrieve_chunks
from reranker import model

question = "What was the EASI-75 response rate at week 16 in SOLO 1 and SOLO 2 for patients receiving weekly dupilumab, and how do these compare to placebo?"

chunks = retrieve_chunks(question)

pairs = [
    (question, chunk["content"]["text"])
    for chunk in chunks
]

scores = model.predict(pairs)

reranked = []

for original_rank, (chunk, score) in enumerate(
    zip(chunks, scores),
    start=1
):
    reranked.append({
        "original_rank": original_rank,
        "score": float(score),
        "text": chunk["content"]["text"]
    })

reranked.sort(
    key=lambda x: x["score"],
    reverse=True
)

for rerank_rank, result in enumerate(reranked, start=1):
    print(f"\n--- CrossEncoder Rank {rerank_rank} ---")
    print("Original Bedrock Rank:", result["original_rank"])
    print("CrossEncoder Score:", result["score"])
    print("Text:", result["text"])