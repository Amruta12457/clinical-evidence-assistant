# Design Decisions  

## Chunking Strategy

Strategy:
Semantic chunking

Initial configuration:
- Max buffer size: 0.5
- Maximum chunk size: 512 tokens
- Breakpoint threshold: 90%

Rationale:
Semantic chunking was selected because the knowledge base
contains long, information-dense clinical documents. The goal
is to create semantically coherent retrieval units rather than
arbitrarily splitting documents by token count.

These parameters are initial experimental values and will be
evaluated against the project's retrieval evaluation set.