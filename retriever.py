import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS
import re


# Studio track names as they appear in the related_studio metadata field.
# Used to detect track-specific queries and apply metadata filtering.
_TRACK_NAMES = {
    "product studio": "Product Studio",
    "startup studio": "Startup Studio",
    "bigco studio": "BigCo Studio",
    "pitech": "PiTech Impact Studio",
    "pitech impact studio": "PiTech Impact Studio",
}


def _build_where_filter(query: str):
    """
    Inspect the query for year mentions and Studio track names.
    Return a ChromaDB `where` filter dict if either is found, else None.

    Examples:
      "Who won the 2026 Startup Awards?"
        → {"year": {"$eq": "2026"}}
      "How does Product Studio team formation work?"
        → {"related_studio": {"$eq": "Product Studio"}}
      "Who won the 2026 Product Studio awards?"
        → {"$and": [{"year": {"$eq": "2026"}},
                    {"related_studio": {"$eq": "Product Studio"}}]}
      "How does teaming work?"
        → None  (no filter, full-corpus search)

    Design note: filtering trades recall for precision. We only filter when
    the query contains an explicit signal (a year number or a known track name)
    — ambiguous queries always fall back to full-corpus search.
    """
    query_lower = query.lower()

    # Detect a 4-digit year between 2015 and 2030
    year_match = re.search(r'\b(20[12][0-9])\b', query)
    year_filter = {"year": {"$eq": year_match.group(1)}} if year_match else None

    # Detect a known Studio track name
    track_filter = None
    for keyword, canonical in _TRACK_NAMES.items():
        if keyword in query_lower:
            # Use $contains instead of $eq so that multi-track documents
            # (e.g. "Product Studio / Startup Studio / BigCo Studio") are
            # also matched when filtering by a specific track name.
            track_filter = {"related_studio": {"$contains": canonical}}
            break

    if year_filter and track_filter:
        return {"$and": [year_filter, track_filter]}
    return year_filter or track_filter
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client initialized once at module load.
# sentence-transformers downloads the model (~80MB) on first use — cached afterward.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return _collection


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in ChromaDB.

    Each chunk dict must have: text, source, year, related_studio, chunk_id.
    year and related_studio are stored as metadata alongside source so the
    retriever can surface them for citation and future metadata filtering.
    ChromaDB's embedding function converts text to vectors automatically.
    """
    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{
            "source": c["source"],
            "year": c.get("year", "Unknown"),
            "related_studio": c.get("related_studio", "Unknown"),
        } for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    """
    Find the most relevant chunks for a user's query using semantic search.

    Uses _collection.query() with cosine distance. Returns results ordered
    from most to least relevant (lowest to highest distance score).

    Metadata filtering (automatic, query-driven):
    - If the query contains a year (e.g. "2026"), only chunks from that year
      are searched. This prevents the 2025 Startup Awards document from
      outranking the 2026 document on a "2026 winners" query.
    - If the query names a Studio track (e.g. "Product Studio"), only chunks
      from that track are searched. This prevents cross-track contamination
      (e.g. Startup Studio teaming content appearing in a Product Studio query).
    - If neither signal is found, full-corpus search runs as normal.

    Falls back to full-corpus search if the filtered result set is empty
    (e.g. user asks about a year with no matching documents).

    Returns a list of dicts: {text, source, year, related_studio, distance}
    """
    if _collection.count() == 0:
        return []

    where = _build_where_filter(query)

    def _query(where_clause):
        return _collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
            where=where_clause,
        )

    if where:
        print(f"  [retriever] applying filter: {where}")
        results = _query(where)
        # If the filter returns nothing, fall back to unfiltered search
        if not results["documents"][0]:
            print(f"  [retriever] filter returned 0 results, falling back to full search")
            results = _query(None)
    else:
        results = _collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": meta.get("source", "Unknown"),
            "year": meta.get("year", "Unknown"),
            "related_studio": meta.get("related_studio", "Unknown"),
            "distance": round(dist, 4),
        })

    return chunks