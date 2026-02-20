# AI-Driven Chunking

Overview
--------
AI-driven chunking uses a large language model (LLM) to split a document into semantically coherent pieces. LLM detect natural breakpoints in the text, ensuring each chunk encapsulates complete ideas. It is asked to return a JSON array of text chunks; the code then converts each chunk into a `Document` with helpful metadata for retrieval and filtering.

This repository includes a mock local implementation for experimentation and a production-ready pattern for integrating with a hosted LLM (Databricks in the example).

Quick Start
-----------
Run the example (mock mode):

```bash
python3 chunking/ai_driven_chunking.py
```

When used with a real LLM, configure your endpoint and credentials before running.

Prompt Template (example)
-------------------------
The LLM is instructed with a prompt that asks for a JSON array of at most `{max_chunks}` strings. Example prompt (trimmed):

```jinja
You are a document processing expert. Your task is to break down the following document into
at most {max_chunks} meaningful chunks. Follow these guidelines:

1. Each chunk should contain complete ideas or concepts
2. More complex sections should be in smaller chunks
3. Preserve headers with their associated content
4. Keep related information together
5. Maintain the original order of the document

DOCUMENT:
{document}

Return ONLY a valid JSON array of strings, where each string is a chunk.
```

LLM Configuration (example)
---------------------------
The example uses `ChatDatabricks` (Databricks LLM). Example parameters:

```python
llm = ChatDatabricks(
    endpoint="databricks-meta-llama-3-3-70b-instruct",
    temperature=0.1,
    max_tokens=4000
)
```

Processing flow
---------------
1. Invoke the prompt/LLM chain with the document and `max_chunks`.
2. Extract the JSON array from the model's response (the code searches for a JSON array in the LLM output).
3. Parse the array and convert each string into a `Document(page_content=..., metadata={...})`.
4. Compute lightweight analytics for each chunk (word counts, unique words, word density, document position) and store in metadata.

Example metadata for each chunk:

```json
{
  "chunk_id": 0,
  "total_chunks": 8,
  "chunk_size": 1238,
  "chunk_type": "ai_driven",
  "document_position": 0.0,
  "word_count": 145,
  "unique_words": 56,
  "word_density": 0.39
}
```

Local mock mode
---------------
If you do not have a Databricks endpoint available, the repository includes `perform_ai_driven_chunking_mock()` which performs paragraph-based chunking and produces the same `Document`-style outputs for local testing.

Notes & Best Practices
----------------------
- Ask the model to return only a JSON array to simplify parsing. Guard the parser by extracting the first JSON-like array when needed.
- Keep `temperature` low (e.g., `0.0–0.2`) so the model's output is deterministic and parsable.
- Validate and sanitize model output before parsing. The current code uses a regex to find a JSON array and then `json.loads`.
- Store important metadata fields (e.g., `chunk_type`, `chunk_id`, `document_position`) to support filtering during retrieval.

Troubleshooting
---------------
- If the LLM returns extra text around the JSON, the regex extractor should find the array. If parsing still fails, inspect `response.content` for formatting issues.
- For long documents, increase `max_tokens` or use streaming / chunked prompting.

See also
--------
- The mock function in `chunking/ai_driven_chunking.py` for a runnable local example.
- Other chunker strategies in `chunking/` (fixed-size, semantic, adaptive, context-enriched).

Pros & Cons
-----------
Pros:
- Produces semantically coherent chunks that align with conceptual boundaries.
- Can preserve headers and group related content intelligently.

Cons:
- Requires an LLM (cost and latency) and reliable parsing of model output.
- Model output can vary; you must validate and sanitize the JSON responses.

