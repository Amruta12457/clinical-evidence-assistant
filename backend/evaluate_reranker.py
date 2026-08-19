from bedrock import retrieve_chunks
from reranker import rerank
from benchmark import benchmark


for item in benchmark:

    question = item["question"]

    print(f"\n=== {item['id']} ===")
    print(question)

    chunks = retrieve_chunks(question)

    # Find the original Bedrock rank of the answer-bearing chunk
    original_rank = None

    for rank, chunk in enumerate(chunks, start=1):

        if all(
            evidence.lower() in chunk["content"]["text"].lower()
            for evidence in item["answer_evidence"]
        ):
            original_rank = rank
            break

    # CrossEncoder reranking
    reranked = rerank(question, chunks)

    # Find the CrossEncoder rank of the answer-bearing chunk
    rerank_rank = None

    for rank, result in enumerate(reranked, start=1):

        if all(
            evidence.lower() in result["chunk"]["content"]["text"].lower()
            for evidence in item["answer_evidence"]
        ):
            rerank_rank = rank
            break

    print(f"Bedrock rank: {original_rank}")
    print(f"CrossEncoder rank: {rerank_rank}")