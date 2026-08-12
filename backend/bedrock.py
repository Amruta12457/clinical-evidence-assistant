import boto3

REGION = "us-east-2"
KNOWLEDGE_BASE_ID = "0FPEUMQSVT"

client = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

MODEL_ID = "amazon.nova-lite-v1:0"


def ask_question(question):
    # Send the question to the Bedrock Knowledge Base
    response = client.retrieve_and_generate(
    input={
        "text": question
    },
    retrieveAndGenerateConfiguration={
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": KNOWLEDGE_BASE_ID,
            "modelArn": f"arn:aws:bedrock:{REGION}::foundation-model/{MODEL_ID}"
        }
    })

    return parse_response(response)

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
                sources.append({"document": name, "page_number": page_number, "text": text})
        

    return {
        "answer": answer,
        "sources": sources
    }