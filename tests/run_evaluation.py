"""
Milestone 6 — Evaluation runner
Run from project root: python tests/run_evaluation.py

Runs all 6 evaluation questions and prints full answers + sources.
Copy the output into README.md Evaluation Report.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retriever import retrieve
from generator import generate_response

QUESTIONS = [
    "What are the team size requirements for Startup Studio?",
    "What BigCo companies are partnering with Cornell Tech in 2026?",
    "Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive?",
    "I want to start my own company after graduation. Which Studio track should I choose and why?",
    "What do students say are the weaknesses of the Studio program?",
    "What is the weekly class schedule and structure of PiTech Impact Studio?",
]

def main():
    for i, q in enumerate(QUESTIONS, 1):
        print("=" * 70)
        print(f"Q{i}: {q}")
        print("=" * 70)

        chunks = retrieve(q)
        result = generate_response(q, chunks)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for s in result["sources"]:
            print(f"  • {s}")

        print("\nRETRIEVED CHUNKS (distances):")
        for j, c in enumerate(chunks, 1):
            flag = "✅" if c["distance"] < 0.5 else "⚠️"
            print(f"  {j}. {flag} {c['source']} ({c['year']}) — dist: {c['distance']}")

        print()

if __name__ == "__main__":
    main()