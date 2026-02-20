# Recursive / Code Chunking

Overview
--------
Language-aware recursive chunking is tailored for code and technical content. The splitter attempts larger structural breaks (classes, functions) before falling back to smaller boundaries, and emits metadata such as `structure_name` and `chunk_type`.

Quick start
-----------
```bash
python3 chunking/recursive_chunking.py
```

Processing flow
---------------
- Use `RecursiveCharacterTextSplitter.from_language(...)` for known languages (Python, JS, Java, Go, Rust).
- Split the code/document; detect functions, classes, and imports via regex and add as metadata.
- Produce `Document` objects with `metadata` fields like `chunk_type` (e.g., `function`, `class`, `import`) and `structure_name`.

Notes & tips
-----------
- Example input: `docs/chunking/recursive_chunking/python_code.md`.
- Useful metadata for code search: `structure_name`, `language`, and `lines`.
- Output file: `docs/chunking/recursive_chunking/chunk_output.txt`.

See also
--------
- Combine with semantic chunking for mixed text+code documents.

Pros & Cons
-----------
Pros:
- Preserves functions, classes, and imports as metadata which is valuable for code search and retrieval.
- Language-aware splitting yields more meaningful code chunks than generic splitters.

Cons:
- Heuristics are language-specific and may mis-detect structures for unusual code styles.
- Requires additional handling for mixed text/code documents and language detection.
