# 03 - Embedding & Store (Notes)

This file contains notes and recommended next steps for creating embeddings and storing them for retrieval.

Local exploration steps (high-level):

1. Choose an embedding provider (OpenAI, Databricks, or local models).
2. Use the `Document` objects produced by the chunkers and compute embeddings for `page_content`.
3. Store embeddings + metadata in a vector store (Faiss, Chroma, or Databricks Delta + Vector Search).

Important metadata to keep:
- `chunk_id`, `chunk_type`, `section`, `semantic_density`, `text_complexity` (if available)

Next steps I can implement for you:
- A small script that creates embeddings (mocked or real) and stores them in a local Faiss/Chroma index.
- An example of searching and returning top-k chunks with metadata filtering.