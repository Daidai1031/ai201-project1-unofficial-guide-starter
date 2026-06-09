import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retriever import retrieve
from generator import generate_response

query = "Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive?"

# Test with k=8
chunks = retrieve(query, n_results=8)
print(f"Retrieved {len(chunks)} chunks")
for i, c in enumerate(chunks, 1):
    has_names = any(n in c["text"] for n in ["Aiseptor", "Custos", "Kindred", "Lola"])
    print(f"  Result {i} | dist: {c['distance']} | has winner names: {has_names} | {c['source']}")

print()
result = generate_response(query, chunks)
print("ANSWER:")
print(result["answer"])
print()
print("SOURCES:")
for s in result["sources"]:
    print(f"  • {s}")