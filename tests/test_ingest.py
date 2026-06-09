"""
Milestone 3 — Ingestion pipeline test
Run from project root: python tests/test_ingest.py
"""
import sys
import os

# Add project root to path so ingest.py can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import random

from ingest import load_documents, chunk_document


def main():
    # ── Load ──────────────────────────────────────────────────────────────
    docs = load_documents()
    print(f"Documents loaded: {len(docs)}")
    print()

    # ── Chunk ─────────────────────────────────────────────────────────────
    all_chunks = []
    for doc in docs:
        chunks = chunk_document(
            doc["text"], doc["source"], doc["year"], doc["related_studio"]
        )
        all_chunks.extend(chunks)
        print(f"  {doc['source']} ({doc['year']}) [{doc['related_studio']}]: {len(chunks)} chunks")

    print()
    print(f"Total chunks: {len(all_chunks)}")
    print()

    # ── 5 representative chunks ───────────────────────────────────────────
    random.seed(42)
    samples = random.sample(all_chunks, min(5, len(all_chunks)))

    for i, c in enumerate(samples, 1):
        print(f"{'='*60}")
        print(f"Chunk {i} of 5")
        print(f"  Source  : {c['source']}")
        print(f"  Year    : {c['year']}  |  Studio: {c['related_studio']}")
        print(f"  ID      : {c['chunk_id']}")
        print(f"  Length  : {len(c['text'])} chars")
        print(f"{'─'*60}")
        print(c["text"])
        print()

    # ── Basic sanity checks ───────────────────────────────────────────────
    print("="*60)
    print("Sanity checks")
    print("="*60)

    empty = [c for c in all_chunks if len(c["text"].strip()) == 0]
    print(f"  Empty chunks       : {len(empty)}  (should be 0)")

    metadata_leak = [c for c in all_chunks if "Source Type:" in c["text"] or "Source Location:" in c["text"]]
    print(f"  Metadata leakage   : {len(metadata_leak)}  (should be 0)")

    unknown_year = [c for c in all_chunks if c["year"] == "Unknown"]
    print(f"  Unknown year       : {len(unknown_year)}  (should be 0 ideally)")

    unknown_studio = [c for c in all_chunks if c["related_studio"] == "Unknown"]
    print(f"  Unknown studio     : {len(unknown_studio)}  (should be 0 ideally)")

    too_short = [c for c in all_chunks if len(c["text"]) < 60]
    print(f"  Chunks < 60 chars  : {len(too_short)}  (should be 0)")

    print()


if __name__ == "__main__":
    main()