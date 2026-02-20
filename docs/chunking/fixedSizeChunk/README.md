# Fixed-Size Chunking

Purpose: Splits documents into fixed-size character chunks with optional overlap. Useful as a deterministic baseline for embedding and retrieval.

Usage:

```bash
python3 chunking/fixed_size_chunking.py
```

Notes:
- This directory contains `rag_chunking_test_doc.md`, which is the test input used by multiple chunkers.
- Output is written to `docs/chunking/fixedSizeChunk/chunk_output.txt`.