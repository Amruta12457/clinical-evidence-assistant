from bedrock import retrieve_chunks
from reranker import model
from benchmark import benchmark


def is_relevant(text, expected_evidence):
    text = text.lower()

    return all(
        evidence.lower() in text
        for evidence in expected_evidence
    )


for item in benchmark:

    question = item["question"]

    print(f"\n=== {item['id']} ===")
    print(question)

    chunks = retrieve_chunks(question)

    # Original Bedrock ranking
    original_rank = None

    for rank, chunk in enumerate(chunks, start=1):
        text = chunk["content"]["text"]

        if is_relevant(text, item["expected_evidence"]):
            original_rank = rank
            break

    # CrossEncoder reranking
    pairs = [
        (question, chunk["content"]["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    reranked = []

    for original_rank_number, (chunk, score) in enumerate(
        zip(chunks, scores),
        start=1
    ):
        reranked.append({
            "original_rank": original_rank_number,
            "score": float(score),
            "text": chunk["content"]["text"]
        })

    reranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Find relevant chunk after reranking
    rerank_rank = None

    for rank, result in enumerate(reranked, start=1):

        if is_relevant(
            result["text"],
            item["expected_evidence"]
        ):
            rerank_rank = rank
            break

    print(f"Bedrock rank: {original_rank}")
    print(f"CrossEncoder rank: {rerank_rank}")