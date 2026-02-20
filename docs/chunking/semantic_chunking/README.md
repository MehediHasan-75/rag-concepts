# Semantic Chunking

Purpose: Recursive, semantics-first splitting that prefers paragraph and sentence boundaries before falling back to smaller units.

Usage:

```bash
python3 chunking/semantic_chunking.py
```

Notes:
- The module reads `docs/chunking/fixed_size_chunk/rag_chunking_test_doc.md` by default.
- There is no external LLM dependency for basic chunking; outputs are saved for inspection.
