import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingest import load_documents, chunk_document

docs = load_documents()
for doc in docs:
    if "startup_awards_2026" in doc["filename"].lower():
        chunks = chunk_document(doc["text"], doc["source"], doc["year"], doc["related_studio"])
        print(f"Total chunks in 2026 awards doc: {len(chunks)}")
        print()
        for i, c in enumerate(chunks):
            names = ["Aiseptor", "Custos", "Kindred", "Lola", "CoagHealth", "MedComm"]
            has_names = any(n in c["text"] for n in names)
            print(f"Chunk {i} ({len(c['text'])} chars) — contains winner names: {has_names}")
            if has_names:
                print(c["text"])
            print()