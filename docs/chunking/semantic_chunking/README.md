# Semantic Chunking

Overview
--------
Semantic chunking follows a hierarchy of separators (paragraph → line → sentence → word → character) to preserve semantic coherence. It tries larger, meaningful boundaries first to avoid splitting ideas awkwardly.

Quick start
-----------
```bash
python3 chunking/semantic_chunking.py
```

Processing flow
---------------
- Use `RecursiveCharacterTextSplitter` with ordered separators such as `['\n\n', '\n', '. ', ' ', '']`.
- Recursively split until chunks are within `chunk_size`.
- Compute a simple `semantic_density` metric and attach section metadata if a header is detected.

Notes & tips
-----------
- Default input: `docs/chunking/fixed_size_chunk/rag_chunking_test_doc.md`.
- Output file: `docs/chunking/semantic_chunking/chunk_output.txt`.
- Use `semantic_density` to prioritize chunks during retrieval.

See also
--------
- Compare with `fixed_size_chunk` and `adaptive_chunking` to observe differences in chunk boundaries and retrieval behavior.

Pros & Cons
-----------
Pros:
- Prefers meaningful boundaries (paragraphs, sentences), producing semantically coherent chunks.
- Often yields higher-quality embeddings and retrieval results compared to naive fixed-size splits.

Cons:
- More complex splitting logic and variable chunk sizes can complicate embedding budget planning.
- May require tuning of separators and chunk size thresholds for different document types.
