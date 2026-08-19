# RAG System Evaluation Report — Clinical Evidence Chatbot

## Overview

The system was evaluated using a **12-question clinical evidence benchmark** designed to test retrieval quality, answer correctness, source grounding, and reliability.

The questions covered clinical trial design, enrollment, efficacy outcomes, adverse events, long-term safety, and regulatory-label information.

The evaluation was performed in two stages:

1. **Baseline:** Bedrock semantic retrieval
2. **Improved:** Bedrock retrieval → CrossEncoder reranking → generation

---

## 1. Baseline Retrieval Testing

Initial testing revealed that semantic retrieval could return highly relevant clinical information without ranking the **specific evidence needed to answer the question** highly enough.

### Example: Q3 — SOLO 1/2 Enrollment

> *What were the enrollment numbers for SOLO 1 and SOLO 2?*

The exact answer-bearing evidence was initially ranked **9th out of 20 results**.

This demonstrated that the problem was not simply generation quality — the correct evidence existed in the Knowledge Base but was being ranked too low.

### Example: EASI-75 Question

Another important failure occurred with an EASI-75 question. The system retrieved legitimate clinical numbers for a related endpoint (IGA) and used them as if they were EASI-75 results.

This showed that **plausible, semantically related evidence can still produce an incorrect answer.**

---

## 2. CrossEncoder Reranking

A second-stage CrossEncoder reranker was added to the pipeline:

```
Question
   ↓
Bedrock retrieves 20 candidates
   ↓
CrossEncoder reranks candidates
   ↓
Top 10 evidence chunks
   ↓
Nova Lite (generation)
```

**Model used:** `cross-encoder/ms-marco-MiniLM-L6-v2`

The reranker evaluates the question and each candidate chunk together, providing a more targeted relevance score than the initial vector search.

### Before vs. After

| Question | Bedrock Rank | CrossEncoder Rank |
|---|---|---|
| SOLO 1 study design | 9 | 1 |
| SOLO 1/2 enrollment | 9 | 2 |
| OLE enrollment/exposure | 3 | 1 |
| OLE adverse events | 16 | 1 |
| Monotherapy adverse events | 1 | 1 |
| Conjunctivitis comparison | 1 | 1 |

The clearest improvement was **Q3**, where the exact enrollment evidence moved from **rank 9 → rank 2**.

The integrated chatbot then correctly answered:

> SOLO 1: 671 patients
> SOLO 2: 708 patients

---

## 3. End-to-End Testing

After validating the reranker, it was integrated into the actual application and tested through the frontend.

Representative tests included:

- **Q3:** Correctly retrieved and cited SOLO 1/2 enrollment numbers.
- **Q10:** Correctly identified the AD-1225 long-term extension and 260 weeks of safety assessment.
- **Q12:** Tested whether the system would distinguish EASI-75 from related IGA outcomes.

These tests verified that the improved retrieval pipeline affected the actual chatbot rather than only a standalone experiment.

---

## 4. Reliability Testing

Q12 exposed an important remaining limitation: the reranker did not always surface the exact numerical evidence.

Instead of allowing the model to substitute related clinical values, the final pipeline was tested with a larger evidence set and conservative grounding behavior.

The system ultimately responded that the available evidence was insufficient to provide the exact requested EASI-75 rates, rather than presenting unsupported numbers.

This demonstrated an important reliability principle:

> **When the evidence does not support an exact answer, the system should acknowledge the limitation rather than infer from a related clinical measure.**

---

## Key Findings

The evaluation demonstrated that:

- Semantic retrieval can rank related but non-answer-bearing evidence highly.
- CrossEncoder reranking substantially improved the ranking of several answer-bearing chunks.
- Retrieval errors can directly cause generation errors.
- Increasing the evidence set can improve coverage, but also introduces more potential distractors.
- Evidence-grounded generation can prevent unsupported answers when retrieval remains imperfect.

The evaluation therefore served as an engineering feedback loop:

**Identify failure → diagnose retrieval → implement reranking → measure improvement → test remaining failure cases.**

---

## Limitations

This was a targeted 12-question engineering benchmark, not a statistically rigorous clinical validation study. Answer-bearing evidence was identified manually, and some questions have multiple valid supporting chunks.

The goal was to identify and address real retrieval and reliability failure modes rather than claim perfect performance.