import boto3
import os
from dotenv import load_dotenv
from reranker import get_top_chunks

load_dotenv()

REGION = os.getenv("REGION")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

generation_client = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)

MODEL_ID = os.getenv("MODEL_ID")


def ask_question(question):
    chunks = retrieve_chunks(question)

    top_chunks = get_top_chunks(
        question,
        chunks,
        k=5
    )

    context = "\n\n".join(
        f"[Source {i}]\n{chunk['content']['text']}"
        for i, chunk in enumerate(top_chunks, start=1)
    )

    prompt = f"""
    You are a clinical evidence assistant.

    Answer the user's question using only the provided clinical evidence.

    If the evidence does not contain enough information to answer the question,
    say that the available evidence is insufficient. Do not invent or assume
    information.

    User question:
    {question}

    Clinical evidence:
    {context}
    """

    response = generation_client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )

    answer = response["output"]["message"]["content"][0]["text"]

    sources = []

    for i, chunk in enumerate(top_chunks, start=1):
        name = chunk["location"]["s3Location"]["uri"].split("/")[-1]
        page_number = chunk.get("metadata", {}).get(
            "x-amz-bedrock-kb-document-page-number"
        )

        sources.append({
            "rank": i,
            "document": name,
            "page_number": page_number,
            "text": chunk["content"]["text"]
        })

    return {
        "answer": answer,
        "sources": sources
    }

def retrieve_chunks(question):
    response = client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": question
        },
        retrievalConfiguration={
            "vectorSearchConfiguration": {
                "numberOfResults": 20
            }
        }
    )

    return response["retrievalResults"]

def parse_response(response):
    # Extract the generated answer and retrieved source information
    sources = []
    seen = set()
    answer = response["output"]["text"]

    citations = response["citations"]

    for citation in citations:
        for chunk in citation["retrievedReferences"]:
            text = chunk["content"]["text"]
            name = chunk["location"]["s3Location"]["uri"].split("/")[-1]
            page_number = chunk.get("metadata", {}).get("x-amz-bedrock-kb-document-page-number")

            # De-duplication of source text chunks
            key = (name, page_number, text)
            if key not in seen:
                seen.add(key)
                sources.append({"rank": len(sources) + 1, "document": name, "page_number": page_number, "text": text})
        

    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    question = "What was the EASI-75 response rate at week 16 in SOLO 1 and SOLO 2 for patients receiving weekly dupilumab, and how do these compare to placebo?"

    result = ask_question(question)

    print("\n--- ANSWER ---")
    print(result["answer"])

    print("\n--- SOURCES ---")

    for source in result["sources"]:
        print(f"\n--- Source {source['rank']} ---")
        print("Document:", source["document"])
        print("Page:", source["page_number"])
        print("Text:", source["text"])