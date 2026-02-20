# 05 - Generation (Combining Retrieved Context + LLM)

This step shows how to craft a prompt that combines retrieved chunks and the user question.

Simple prompt template:

```
You are an assistant. Use the following context to answer the question.

Context:
{retrieved_chunks}

Question:
{user_question}

Answer concisely, cite relevant chunk_ids if possible.
```

Tips:
- Limit the number of tokens sent to the LLM by truncating or summarizing retrieved chunks.
- Use metadata to prefer high semantic density chunks.

I can add a runnable example that calls a local mock LLM or integrates with a real provider.