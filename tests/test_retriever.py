"""
Milestone 4 — Retrieval test
Run from project root: python tests/test_retriever.py

First run will trigger ingestion into ChromaDB (takes ~1-2 min for embedding).
Subsequent runs skip ingestion if chroma_db/ already exists.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection


# ── Step 1: Ingest if needed ───────────────────────────────────────────────
def maybe_ingest():
    collection = get_collection()
    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        return

    print("Ingesting documents into ChromaDB...")
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(
            doc["text"], doc["source"], doc["year"], doc["related_studio"]
        )
        all_chunks.extend(chunks)
    embed_and_store(all_chunks)
    print()


# ── Step 2: Test retrieval with 3 evaluation queries ──────────────────────
TEST_QUERIES = [
    "What are the team size requirements for Startup Studio?",
    "What BigCo companies are partnering with Cornell Tech in 2026?",
    "Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive?",
    "I want to start my own company after graduation. Which Studio track should I choose and why?",
    "What do students say are the weaknesses of the Studio program?",
    "What is the weekly class schedule and structure of PiTech Impact Studio?",
]

def test_retrieval():
    for query in TEST_QUERIES:
        print("=" * 65)
        print(f"Query: {query}")
        print("=" * 65)

        chunks = retrieve(query)

        for i, c in enumerate(chunks, 1):
            relevance = "✅ good" if c["distance"] < 0.5 else "⚠️  weak"
            print(f"\n  Result {i} {relevance}  |  distance: {c['distance']}")
            print(f"  Source : {c['source']} ({c['year']}) [{c['related_studio']}]")
            print(f"  {'─'*57}")
            # Print full chunk text, indented
            for line in c["text"].splitlines():
                print(f"  {line}")

        # Summary line
        scores = [c["distance"] for c in chunks]
        print(f"\n  → distances: {scores}")
        best = scores[0] if scores else None
        if best is not None and best < 0.5:
            print(f"  → top result looks relevant (distance {best} < 0.5) ✅")
        elif best is not None:
            print(f"  → top result may be weak (distance {best} ≥ 0.5) ⚠️")
        print()


if __name__ == "__main__":
    maybe_ingest()
    test_retrieval()