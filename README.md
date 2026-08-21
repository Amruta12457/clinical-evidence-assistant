# Clinical Evidence Assistant

A deployed retrieval-augmented generation (RAG) system for answering questions about clinical evidence from public medical documents.

The system retrieves relevant evidence from an Amazon Bedrock Knowledge Base, applies a second-stage CrossEncoder reranker to improve evidence ordering, and uses Amazon Nova Lite to generate answers grounded in the retrieved clinical evidence.

The project was built and evaluated around a 12-question clinical evidence benchmark, with particular focus on retrieval quality, source grounding, and behavior when the available evidence is insufficient.

**Live Demo:** https://clinical-evidence-assistant.vercel.app

---

## Architecture

```text
                         User Question
                              │
                              ▼
                    ┌─────────────────────┐
                    │    React + TypeScript│
                    │       Frontend      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    │      POST /ask      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Bedrock Retrieval  │
                    │    Top 20 Chunks    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CrossEncoder      │
                    │      Reranker       │
                    │   Top 10 Chunks     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Amazon Nova Lite  │
                    │      Generation     │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │    Answer    │      │   Evidence   │
             │              │      │   Sources    │
             └──────────────┘      └──────────────┘
```

### Infrastructure

* **Frontend:** React + TypeScript, deployed on Vercel
* **Backend:** FastAPI, deployed on Google Cloud Run
* **Retrieval:** Amazon Bedrock Knowledge Bases
* **Embeddings:** Amazon Titan Text Embeddings V2
* **Reranking:** `cross-encoder/ms-marco-MiniLM-L6-v2`
* **Generation:** Amazon Nova Lite
* **Document storage:** Amazon S3
* **Region:** AWS `us-east-2`

---

## Why Reranking?

A key challenge identified during development was that vector retrieval did not always place the most useful evidence near the top of the retrieved results.

For example, for a question asking for the enrollment numbers in the SOLO 1 and SOLO 2 trials, the exact answer-bearing chunk was originally ranked **9th out of 20 retrieved chunks**.

To address this, the system uses a two-stage retrieval pipeline:

```text
Question
   │
   ▼
Bedrock vector retrieval
   │
   │  Top 20 candidates
   ▼
CrossEncoder reranking
   │
   │  Top 10 evidence chunks
   ▼
Nova Lite
   │
   ▼
Grounded answer + sources
```

The CrossEncoder evaluates each question-document pair directly and reorders the retrieved candidates based on relevance.

This separates **candidate retrieval** from **evidence ranking**, allowing the system to improve retrieval quality without replacing the underlying vector search.

---

## Evaluation

The system was evaluated using a benchmark of **12 clinical evidence questions** covering:

* Clinical mechanism
* Clinical trial design
* Patient enrollment
* Primary and secondary endpoints
* Treatment outcomes
* Long-term safety
* Adverse events
* Comparison of study designs
* Source-specific evidence

The benchmark was used to identify retrieval failures, evaluate reranking behavior, and test whether generated answers remained grounded in the available evidence.

### Retrieval Improvements

| Question                      | Relevant Evidence: Before | After Reranking |
| ----------------------------- | ------------------------: | --------------: |
| SOLO 1 design                 |                        #9 |          **#1** |
| SOLO 1/2 enrollment           |                        #9 |          **#2** |
| Long-term OLE enrollment      |                        #3 |          **#1** |
| Long-term safety events       |                       #16 |          **#1** |
| Clinical trial adverse events |                        #1 |          **#1** |
| Conjunctivitis comparison     |                        #1 |          **#1** |

The reranker was particularly useful for questions where the correct evidence was present in the initial retrieval set but ranked poorly.

### Example: Retrieval Failure

For the SOLO 1/2 enrollment question:

> **Question:** What were the enrollment numbers for SOLO 1 and SOLO 2?

The exact evidence was initially ranked **9th/20** by vector retrieval.

After CrossEncoder reranking:

**2nd/20**

The integrated system then produced the correct answer:

> SOLO 1 enrolled 671 patients and SOLO 2 enrolled 708 patients.

---

## Reliability Testing

Retrieval quality alone does not guarantee a reliable generated answer.

A separate test was performed using a question where the exact requested evidence was poorly represented among the top-ranked chunks.

For the EASI-75 endpoint question, the exact answer-bearing evidence ranked poorly after reranking. Instead of relying on loosely related evidence, the final system was tested with a larger evidence set and an instruction to acknowledge insufficient evidence rather than inventing unsupported values.

This exposed an important limitation of RAG systems:

> **A model can produce a plausible answer even when the retrieved evidence does not directly support the requested claim.**

The system therefore instructs the generator to explicitly state when the provided evidence is insufficient.

---

## Key Findings

The evaluation showed several recurring retrieval and grounding failure modes:

1. **Wrong section retrieved**
   Relevant information existed in the document, but the most useful section was ranked too low.

2. **Correct information, wrong source**
   The system sometimes retrieved the correct fact from a different study or document than the question requested.

3. **Endpoint confusion**
   Related clinical endpoints such as IGA and EASI-75 could be confused when evidence from both appeared in the retrieved context.

4. **Incomplete evidence**
   Some questions required multiple evidence chunks to produce a complete answer.

5. **Insufficient evidence**
   When the exact requested evidence was not sufficiently represented in the retrieved context, the system needed to avoid making unsupported quantitative claims.

These findings motivated the use of second-stage reranking and explicit insufficient-evidence behavior.

---

## Features

* Retrieval-augmented generation using Amazon Bedrock
* Two-stage retrieval with CrossEncoder reranking
* Source-grounded clinical answers
* Document and page-level source information
* Evidence displayed alongside generated answers
* Source deduplication
* REST API using FastAPI
* Pydantic request/response validation
* Environment-based configuration
* Error handling and logging
* Deployed frontend and backend

---

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* boto3
* python-dotenv

### AI / ML

* Amazon Bedrock Knowledge Bases
* Amazon Titan Text Embeddings V2
* Amazon Nova Lite
* Sentence Transformers
* CrossEncoder
* Vector retrieval

### Cloud / Infrastructure

* Amazon S3
* AWS Bedrock
* Google Cloud Run
* Google Artifact Registry
* Vercel

### Frontend

* React
* TypeScript

---

## Project Structure

```text
clinical-evidence-assistant/
│
├── backend/
│   ├── main.py
│   ├── bedrock.py
│   ├── reranker.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── Sources.tsx
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
└── README.md
```

---

## API

### `POST /ask`

Accepts a clinical question and returns a generated answer with supporting evidence.

#### Request

```json
{
  "question": "What were the enrollment numbers for SOLO 1 and SOLO 2?"
}
```

#### Response

```json
{
  "answer": "SOLO 1 enrolled 671 patients and SOLO 2 enrolled 708 patients.",
  "sources": [
    {
      "rank": 1,
      "document": "Phase3_Trials.pdf",
      "page_number": 4,
      "text": "..."
    }
  ]
}
```

### Interactive API Documentation

The deployed FastAPI backend provides interactive Swagger documentation at:

```text
https://clinical-evidence-backend-716383259320.us-east1.run.app/docs
```

---

## Local Development

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd clinical-evidence-assistant
```

### 2. Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Configure environment variables

Create a `.env` file containing:

```text
REGION=us-east-2
KNOWLEDGE_BASE_ID=<your-knowledge-base-id>
MODEL_ID=amazon.nova-lite-v1:0
```

AWS credentials should be configured through the AWS CLI or another supported AWS credential provider.

Do **not** commit AWS credentials or `.env` files to the repository.

### 4. Start the backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Start the frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

The frontend can then be configured to point to the local FastAPI backend using:

```text
VITE_API_URL=http://127.0.0.1:8000
```

---

## Limitations

This project is intended as an engineering and research prototype rather than a clinical decision-support system.

Current limitations include:

* The benchmark contains 12 questions and is not intended to represent comprehensive clinical evaluation.
* Retrieval performance depends on the quality and coverage of the indexed documents.
* The CrossEncoder was trained for general passage ranking rather than specifically for clinical evidence.
* Generated answers are only as reliable as the evidence supplied to the generation model.
* The system does not independently verify claims against external medical databases.
* The underlying clinical documents are public evidence sources and should not be treated as medical advice.

---

## Motivation

Clinical evidence is distributed across research papers, clinical trial reports, regulatory documents, and other lengthy medical sources.

This project explores how retrieval-augmented generation can make clinical evidence easier to access while maintaining a direct connection between generated answers and their underlying sources.

Rather than treating RAG as simply an LLM application, the project focuses on **retrieval quality, evidence ranking, evaluation, and reliability**.

---

## Future Improvements

Potential future work includes:

* Expanding the evaluation benchmark
* Testing domain-specific rerankers
* Evaluating additional retrieval strategies
* Improving evidence coverage for multi-part questions
* Adding automated retrieval and answer-quality metrics
* Adding production monitoring and observability
