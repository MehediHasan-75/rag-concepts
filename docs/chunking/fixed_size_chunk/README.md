# Fixed-Size Chunking

Overview
--------
Deterministically splits a document into fixed-size character chunks with optional overlap. This is a simple baseline useful for reproducible embeddings and debugging retrieval behavior.

Quick start
-----------
```bash
python3 chunking/fixed_size_chunking.py
```

Processing flow
---------------
- Use `CharacterTextSplitter` with `chunk_size` and `chunk_overlap`.
- Split the document, then wrap each chunk into a `Document` with metadata: `chunk_id`, `total_chunks`, `chunk_size`, `chunk_type: "fixed-size"`.

Notes & tips
-----------
- The repo includes a sample input: `docs/chunking/fixed_size_chunk/rag_chunking_test_doc.md`.
- Overlap behavior depends on splitter separators; LangChain overlaps whole pieces defined by separators.
- Output file: `docs/chunking/fixed_size_chunk/chunk_output.txt`.

See also
--------
- Use this as a baseline to compare against semantic or AI-driven chunking.

Pros & Cons
-----------
Pros:
- Simple, deterministic, and fast to run.
- Easy to reproduce and reason about; good baseline for testing.

Cons:
- May split ideas or sentences arbitrarily, reducing semantic coherence.
- Fixed sizes can be suboptimal for heterogeneous documents (mix of code, prose, lists).
