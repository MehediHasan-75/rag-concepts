#!/usr/bin/env bash
# Simple helper to setup and run the example data generation + one chunker
set -e

# 1) Create venv if not present
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Generate test document
python3 chunking/md_generator.py

# 4) Run fixed-size chunking as a quick example
python3 chunking/fixed_size_chunking.py

# 5) Show where outputs are written
echo "Generated document: docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md"
echo "Chunk outputs: docs/chunking/*/chunk_output.txt"

# Deactivate venv
deactivate
