"""
Milestone 5 — Generation test
Run from project root: python tests/test_generator.py

Tests grounded generation on 3 queries + 1 out-of-scope query.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retriever import retrieve
from generator import generate_response

TEST_CASES = [
    {
        "query": "What are the team size requirements for Startup Studio?",
        "expect": "grounded — should cite Slack Startup Team Formation",
    },
    {
        "query": "Who won the 2026 Cornell Tech Startup Awards?",
        "expect": "grounded — should cite Official Startup Awards 2026",
    },
    {
        "query": "What is the weekly class schedule of PiTech Impact Studio?",
        "expect": "should acknowledge lack of direct info, not fabricate a schedule",
    },
    {
        "query": "What is the best pizza place near Cornell Tech campus?",
        "expect": "out-of-scope — should decline, not answer from general knowledge",
    },
]


def main():
    for i, case in enumerate(TEST_CASES, 1):
        print("=" * 65)
        print(f"Test {i}: {case['query']}")
        print(f"Expected behavior: {case['expect']}")
        print("─" * 65)

        retrieved = retrieve(case["query"])
        result = generate_response(case["query"], retrieved)

        print("ANSWER:")
        print(result["answer"])
        print()
        print("SOURCES:")
        for s in result["sources"]:
            print(f"  • {s}")
        print()

        print("Grounding check — ask yourself:")
        print("  1. Could this answer have come from outside the retrieved chunks?")
        print("  2. Are sources cited inline in the answer text?")
        print("  3. Does the sources box match what the answer references?")
        print()


if __name__ == "__main__":
    main()