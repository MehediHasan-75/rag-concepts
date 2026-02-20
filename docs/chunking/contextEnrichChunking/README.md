# Context-Enriched Chunking

Purpose: Produces chunks augmented with contextual summaries from neighboring chunks to preserve local context for retrieval or downstream QA.

Usage:

```bash
python3 chunking/context_enrich_chunking.py
```

Notes:
- A mock summarizer is provided for local testing. Replace with a real LLM chain for production.
- Output is written to `docs/chunking/contextEnrichChunking/chunk_output.txt`.