# 02 - Chunking Overview and Exercises

This guide shows how to run and compare the chunkers available in the `chunking/` folder.

Run these and inspect the `docs/chunking/*/chunk_output.txt` files:

- Fixed-size chunking:

```bash
python3 chunking/fixed_size_chunking.py
```

- Semantic chunking:

```bash
python3 chunking/semantic_chunking.py
```

- Adaptive chunking:

```bash
python3 chunking/adaptive_chunking.py
```

- AI-driven chunking (mock):

```bash
python3 chunking/ai_driven_chunking.py
```

Exercises:
- Compare `chunk_size` and `chunk_type` metadata across outputs.
- Find where the injected target facts land and see which chunker keeps the fact intact.
- Try changing `chunk_size` and `chunk_overlap` values and observe differences.