# Adaptive Chunking

Purpose: Adaptive chunking splits text into variable-sized chunks based on estimated text complexity (lexical density and sentence length).

Usage:

- Run the module to produce chunked outputs and metadata:

```bash
python3 chunking/adaptive_chunking.py
```

Notes:
- Output is saved to `docs/chunking/adaptiveChunking/chunk_output.txt` when run from the repository root.
- Intended to produce `Document` objects compatible with LangChain workflows.