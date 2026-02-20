# 04 - Retrieval & Augmentation

Overview:

- Retrieval: query the vector store to return relevant chunks for a user query.
- Augmentation: use the retrieved chunks to build a context prompt for the LLM.

Simple workflow:
1. Create embeddings for all chunk documents.
2. Run nearest-neighbor search for the user query.
3. Optionally filter by metadata (e.g., `chunk_type == 'semantic'`).
4. Concatenate top-k chunk `page_content` + user question into a prompt.
5. Call your LLM to generate the answer.

If you'd like, I can add a runnable script that uses a mock embedding (random vectors) and Faiss/Chroma to demonstrate retrieval locally.