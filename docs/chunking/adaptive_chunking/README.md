# Adaptive Chunking

Overview
--------
Adaptive chunking adjusts chunk sizes based on estimated text complexity (e.g., lexical density and sentence length). Complex passages are split into smaller chunks while simpler passages get larger chunks. This helps preserve semantic granularity where it matters.

Quick start
-----------
```bash
python3 chunking/adaptive_chunking.py
```

Processing flow
---------------
- Tokenize the document into sentences.
- Measure complexity per sentence (lexical density, average sentence length).
- Compute adaptive chunk size and overlap based on complexity scores.
- Emit chunks as `Document` objects with `metadata` including `chunk_type: "adaptive"`, `text_complexity`, and sizing metrics.

Example metadata
----------------
```json
{
	"chunk_id": 0,
	"total_chunks": 28,
	"chunk_size": 344,
	"chunk_type": "adaptive",
	"text_complexity": 0.77
}
```

Notes & tips
-----------
- Tune `min_chunk_size`, `max_chunk_size`, `min_chunk_overlap`, and `max_chunk_overlap` for your data.
- The implementation uses NLTK for sentence tokenization; ensure `punkt` is available (`nltk.download('punkt')`).
- Output file: `docs/chunking/adaptive_chunking/chunk_output.txt`.

See also
--------
- Other chunkers in `chunking/` for comparison: fixed-size, semantic, AI-driven, context-enriched.

Pros & Cons
-----------
Pros:
- Adapts chunk size to text complexity, preserving semantic granularity where needed.
- Reduces information loss in dense sections by creating smaller chunks.

Cons:
- More parameters to tune (min/max sizes, overlaps, complexity measure).
- Slightly slower and more complex than fixed-size splitters; depends on NLTK for sentence tokenization.
