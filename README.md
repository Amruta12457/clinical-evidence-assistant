# Clinical Evidence Assistant

A retrieval-augmented generation (RAG) chatbot for answering questions about clinical evidence from public medical documents.

The application uses Amazon Bedrock Knowledge Bases to retrieve relevant evidence from indexed clinical documents and Amazon Nova Lite to generate source-grounded answers.

## Architecture

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │     (planned)       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │                     │
                    │     POST /ask       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Amazon Bedrock    │
                    │  RetrieveAndGenerate│
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐   ┌─────────────────┐
          │ Bedrock         │   │ Amazon Nova     │
          │ Knowledge Base  │   │ Lite            │
          │                 │   │                 │
          │ Retrieval       │   │ Generation      │
          └────────┬────────┘   └─────────────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Clinical        │
          │ Documents in S3 │
          └─────────────────┘
````

## Features

* Retrieval-augmented generation using Amazon Bedrock
* Source-grounded answers from clinical documents
* Document and page-level source information
* Automatic source deduplication
* REST API built with FastAPI
* Request and response validation using Pydantic
* Environment-based configuration
* Error handling and application logging

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* boto3
* python-dotenv

### AI / Cloud

* Amazon Bedrock Knowledge Bases
* Amazon Nova Lite
* Amazon S3
* Vector search

### Frontend

* React + TypeScript (planned)

## Project Structure

```text
clinical-evidence-assistant/
├── .env
├── .env.example
├── .gitignore
├── README.md
│
└── backend/
    ├── main.py
    ├── bedrock.py
    ├── requirements.txt
    └── .venv/
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd clinical-evidence-assistant
```

### 2. Create a Python virtual environment

From the `backend` directory:

```bash
cd backend
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
REGION=us-east-2
KNOWLEDGE_BASE_ID=<your-knowledge-base-id>
MODEL_ID=amazon.nova-lite-v1:0
```

Do not commit `.env` or AWS credentials to GitHub.

### 5. Configure AWS credentials

The application uses boto3 to communicate with AWS.

Configure your AWS credentials using the AWS CLI or another supported AWS credential provider.

For example:

```bash
aws configure
```

Do not place AWS access keys or secret keys directly in the source code.

### 6. Start the backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API should start at:

```text
http://127.0.0.1:8000
```

## API

### POST `/ask`

Accepts a clinical question and returns a generated answer along with retrieved sources.

#### Request

```json
{
  "question": "What is dupilumab?"
}
```

#### Response

```json
{
  "answer": "Dupilumab is ...",
  "sources": [
    {
      "document": "example.pdf",
      "page_number": 2,
      "text": "..."
    }
  ]
}
```

### Interactive API Documentation

Once the backend is running, FastAPI provides interactive documentation at:

```text
http://127.0.0.1:8000/docs
```

## Development

The backend separates responsibilities between the API layer and the Bedrock integration.

### `main.py`

Responsible for:

* Defining API endpoints
* Validating requests
* Validating responses
* Handling HTTP-level errors
* Logging failed requests

### `bedrock.py`

Responsible for:

* Communicating with Amazon Bedrock
* Sending questions to the Knowledge Base
* Parsing Bedrock responses
* Extracting retrieved source information
* Deduplicating source chunks

## Current Status

### Completed

* [x] Amazon Bedrock Knowledge Base
* [x] Clinical document ingestion
* [x] RAG question answering
* [x] Source extraction
* [x] Source deduplication
* [x] FastAPI backend
* [x] Pydantic request/response models
* [x] Error handling and logging
* [x] Environment-based configuration
* [x] Dependency management

### Planned

* [ ] React frontend
* [ ] Connect React frontend to FastAPI
* [ ] Interactive source/citation display
* [ ] Retrieval quality improvements
* [ ] Evaluation dataset
* [ ] Retrieval and answer-quality metrics
* [ ] Deployment

## Motivation

Clinical evidence is distributed across large research papers, trial reports, and other medical documents. Finding relevant evidence can require manually searching through lengthy documents.

This project explores how retrieval-augmented generation can make clinical evidence easier to access while maintaining a connection between generated answers and their underlying sources.


```
