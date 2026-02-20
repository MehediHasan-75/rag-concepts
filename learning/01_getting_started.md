# 01 - Getting Started

Steps to set up and generate the sample document used across chunkers.

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate the synthetic test document used by chunkers:

```bash
python3 chunking/md_generator.py
```

3. Inspect the generated file:

```bash
less docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md
```

Next: run the chunkers in `chunking/` to see how each strategy splits the document.