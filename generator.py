from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

# Chunks with cosine distance above this threshold are considered weak matches.
# For all-MiniLM-L6-v2 with cosine distance, scores above ~0.6 indicate
# the retrieved chunk is not meaningfully related to the query.
DISTANCE_THRESHOLD = 0.6


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved Studio Guide chunks.

    Returns a dict with two keys:
      - "answer"  : the LLM's grounded response string
      - "sources" : list of unique "Source (Year)" strings for UI display

    Grounding mechanism:
    - System prompt explicitly forbids answering outside the provided context.
    - Chunks above DISTANCE_THRESHOLD are filtered before building context,
      preventing weak matches from misleading the model.
    - Each chunk is labeled [Source N: name (year)] so the LLM can cite
      exactly which document each fact came from.
    - Source attribution is also surfaced programmatically: the sources list
      is built from chunk metadata independently of what the LLM writes,
      guaranteeing attribution even if the model forgets to cite inline.
    """
    fallback_sources = []

    if not retrieved_chunks:
        return {
            "answer": (
                "I couldn't find anything relevant in the Studio Guide documents. "
                "Try rephrasing your question or ask about a specific Studio track "
                "(Product Studio, Startup Studio, BigCo Studio, or PiTech Impact Studio)."
            ),
            "sources": fallback_sources,
        }

    # Filter out weak matches
    strong_chunks = [c for c in retrieved_chunks if c["distance"] <= DISTANCE_THRESHOLD]

    if not strong_chunks:
        return {
            "answer": (
                "I found some documents but none were closely relevant to your question. "
                "The Studio Guide covers Cornell Tech's Studio curriculum — try asking about "
                "team formation, Startup Awards, specific Studio tracks, or partner companies."
            ),
            "sources": fallback_sources,
        }

    # Build context block — label each chunk with source and year
    context_parts = []
    for i, chunk in enumerate(strong_chunks, 1):
        year = chunk.get("year", "Unknown")
        label = f"{chunk['source']} ({year})"
        context_parts.append(f"[Source {i}: {label}]\n{chunk['text']}")
    context_block = "\n\n---\n\n".join(context_parts)

    # Build deduplicated sources list for UI display (programmatic, not LLM-generated)
    seen = set()
    sources = []
    for chunk in strong_chunks:
        label = f"{chunk['source']} ({chunk.get('year', 'Unknown')})"
        if label not in seen:
            seen.add(label)
            sources.append(label)

    system_prompt = """You are an assistant for Cornell Tech's Studio program — an unofficial guide that answers questions about Studio courses, team formation, Startup Awards, and partner companies.

STRICT GROUNDING RULES:
1. Answer ONLY using information explicitly stated in the provided context documents.
2. Do NOT use any general knowledge about Cornell Tech, universities, or startups that is not in the context.
3. Always cite which source(s) your answer draws from, using the [Source N: name] labels provided.
4. If multiple sources say different things (e.g., a 2019 document vs. a 2026 document), note the difference and cite both, flagging which is more recent.

HANDLING SPARSE COVERAGE:
5. If the context does not contain direct information about the specific Studio track the user asked about (e.g., PiTech Impact Studio), do NOT silently substitute information from a different track. Instead:
   - First, explicitly acknowledge: "The documents I have don't contain direct information about [track name] on this topic."
   - Then, if related information from another track is present and potentially useful, offer it with a clear caveat: "However, here is how [other track] handles this, which may serve as a reference point..."
   - Do not present information about one Studio track as if it applies to another.
6. If the context contains no relevant information at all, respond with: "The Studio Guide documents I have don't contain enough information to answer that. You may want to check the Cornell Tech website directly or ask a current student.\""""

    user_message = f"""Context documents:

{context_block}

---

Question: {query}

Answer the question using only the context above. Cite your sources using the [Source N] labels.

Format the answer in clean Markdown:
- Use short paragraphs or bullet points when it improves readability.
- Bold only the key answer words or phrases that directly answer the user's question, using **double asterisks**.
- Do not bold whole sentences, source citations, filler words, or every occurrence of a repeated term.
- Keep all other text in normal weight.
- Keep source citations readable and close to the claims they support."""

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
    }
