# Context-Enriched Chunking

Overview
--------
Context-enriched chunking augments each chunk with summaries (or raw text) from neighboring chunks. This preserves local context which is helpful for QA or when retrieved chunks alone lack sufficient background.

Quick start
-----------
```bash
python3 chunking/context_enrich_chunking.py
```

Processing flow
---------------
- Split the document into base chunks (e.g., RecursiveCharacterTextSplitter).
- For each chunk, assemble a window of neighboring chunks (configurable `window_size`).
- Optionally summarize the window with an LLM and attach the summary as `metadata['context']`.
- Emit enriched `Document` objects where `page_content` contains the context and the chunk content.

Notes & tips
-----------
- Use the mock summarizer (`perform_context_enriched_chunking_mock`) for local testing without an LLM.
- When using a real LLM, keep `max_tokens` and prompt length in mind.
- Output file: `docs/chunking/context_enrich_chunking/chunk_output.txt`.

See also
--------
- Useful when retrieved chunks require short summaries to fit LLM prompt size limits.

Pros & Cons
-----------
Pros:
- Preserves and surfaces local context which improves downstream QA and reasoning.
- Can reduce hallucination by providing surrounding background to the LLM.

Cons:
- Increases token usage (larger prompts) and storage size due to redundant context.
- Summarization step may introduce errors if the summarizer is weak or misconfigured.
