# Week 3 — Retrieval-Augmented Generation (RAG)

## Overview

Week 3 extends the e-commerce dispute and resolution platform with a policy-grounded RAG capability.

The implementation covers:

- Markdown policy knowledge-base loading
- Structure-aware chunking
- Sentence-transformer embeddings
- FAISS vector retrieval
- Metadata-aware retrieval
- Similarity-threshold rejection
- Context construction with provenance
- Grounded prompt construction
- Local LLM generation through an OpenAI-compatible endpoint
- Deterministic grounding checks for evaluated forbidden claims
- Retrieval and generation evaluation
- Failure logging
- FastAPI integration

## Knowledge Base

The project uses five training policy documents:

- `payment_policy.md`
- `refund_policy.md`
- `return_policy.md`
- `delivery_policy.md`
- `vendor_payout_policy.md`

Each document carries structured metadata such as document type, domain, version, and status.

The rebuilt knowledge base contains:

- Documents: 5
- Chunks: 35
- Embedding dimension: 384
- Vector index: FAISS `IndexFlatIP`

Embeddings are normalized, so inner-product similarity is used as a cosine-similarity proxy.

## Document Processing

The document layer is structure-aware.

Markdown H2 sections are preserved as logical sections. Large sections are split into bounded chunks with local overlap while retaining:

- document ID
- source filename
- section
- section metadata

The loader stores relative source filenames such as `payment_policy.md`, which preserves provenance through retrieval and generation.

## Retrieval

The application retrieval layer supports:

- `top_k`
- exact metadata filtering
- minimum similarity score (`min_score`)

The retrieval experiment compared Top-K values of 1, 3, and 5 with and without metadata filtering.

### Retrieval findings

All five answerable evaluation cases achieved:

- Source Hit@K: 100%
- Section Hit@K: 100%

across the tested configurations.

However, metadata filtering reduced cross-domain contamination. For example, an unfiltered payment query could retrieve a refund-policy chunk, while the same query with a payment-domain filter stayed within payment-policy chunks.

Therefore, metadata filtering is useful even when binary Hit@K metrics do not change.

## Similarity Threshold

A threshold experiment was performed with:

- 0.40
- 0.45
- 0.50
- 0.55
- 0.60

Results on the current evaluation set:

| Threshold | Answerable retention | Unsupported rejection |
|---:|---:|---:|
| 0.40 | 100% | 0% |
| 0.45 | 100% | 0% |
| 0.50 | 100% | 0% |
| 0.55 | 100% | 100% |
| 0.60 | 100% | 100% |

The implemented retrieval gate therefore uses `min_score = 0.55`.

This threshold is an empirical result for the current small evaluation set, not a universal similarity threshold.

## Context and Prompting

Retrieved chunks are converted into a bounded context containing source, section, similarity score, and text.

The generation prompt requires the model to:

- use only retrieved policy evidence
- avoid unsupported assumptions
- abstain when evidence is insufficient
- avoid inventing deadlines, amounts, guarantees, refunds, compensation, or escalations
- cite the exact source filename and section

## Generation

Generation uses a local Mistral 7B Instruct model through an OpenAI-compatible LM Studio endpoint.

The model is configured without a system-role message because the selected model/template accepts only user and assistant roles. The implementation therefore merges the system instructions appropriately for that provider.

## Grounding Evaluation

A deterministic `GroundingGuard` was implemented for the evaluation framework.

A real generation test exposed an unsupported model-added claim:

> follow the applicable refund procedure

The retrieved payment-policy evidence did not support that step.

The evaluation guard correctly classified the output as blocked and converted it to a safe refusal.

This illustrates an important separation:

- Retrieval can be relevant.
- Generation can still introduce unsupported claims.
- Retrieval quality and generation grounding are separate evaluation concerns.

The current deterministic guard is intentionally limited: it detects explicit configured forbidden claims. It is not a general semantic entailment engine.

## Evaluation Artifacts

The following artifacts are maintained under `data/evaluation/`:

- `rag_eval.json`
- `rag_answer_eval.json`
- `rag_retrieval_comparison.json`
- `rag_threshold_comparison.json`
- `rag_failure_log.json`

The retrieval evaluations measure source and section hit rates. Generation evaluations measure required claims, forbidden claims, abstention behavior, and grounding-block status.

## API

The RAG capability is exposed through:

`POST /api/v1/rag/query`

The API accepts a policy question and returns:

- generated answer
- retrieved sources
- retrieved chunk count
- grounding-block status
- grounding violations

FastAPI API tests use a fake RAG service so they do not depend on slow local LLM inference.

## Current Architecture

```text
Policy Markdown
      |
      v
Markdown Loader
      |
      v
Structure-aware Chunker
      |
      v
SentenceTransformer
      |
      v
FAISS Vector Index
      |
      v
Retriever
  - metadata filter
  - min_score = 0.55
      |
      v
Context Builder
      |
      v
Grounded Prompt
      |
      v
Local Mistral / LM Studio
      |
      v
Grounding Evaluation / Safe Response
      |
      v
FastAPI /api/v1/rag/query
```

## Known Limitations

The current evaluation set is intentionally small and uses five answerable scenarios plus an unsupported scenario.

The `0.55` threshold is therefore calibrated only for this dataset.

The deterministic grounding guard also relies on explicit forbidden-claim phrases during evaluation and should not be described as a complete semantic grounding solution.

These limitations are recorded rather than hidden.

## Week 3 Completion Criteria

Week 3 is complete when:

- RAG document ingestion is implemented
- embeddings and vector retrieval are implemented
- metadata filtering is implemented
- retrieval evaluation is documented
- similarity-threshold behavior is evaluated
- unsupported retrieval can abstain before generation
- generation is integrated with the API
- grounding behavior is evaluated
- known failures are logged
- RAG API tests pass
- full test suite passes
- CI is green
- Week 3 changes are committed and pushed
