import os
import re
from config import DOCS_PATH


def load_documents():
    """
    Load all .md documents from the documents folder.
    Skips .gitkeep and any non-.md files.

    For each document:
      1. Extract Year and Related Studio from the raw header BEFORE cleaning.
      2. Clean the text: strip metadata lines, boilerplate headers,
         image tags, HTML tags, and collapse excess blank lines.
      3. Return structured dicts ready for chunking.

    Returns a list of dicts with keys:
        source, filename, text, year, related_studio
    """
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(DOCS_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        # Step 1: extract metadata before cleaning removes those lines
        year_match = re.search(r'^Year:\s*(.+)$', raw, re.MULTILINE)
        studio_match = re.search(r'^Related Studio:\s*(.+)$', raw, re.MULTILINE)
        year = year_match.group(1).strip() if year_match else "Unknown"
        related_studio = studio_match.group(1).strip() if studio_match else "Unknown"

        # Step 2: clean
        text = raw
        text = re.sub(r'^(Source Type|Source Location|Year|Related Studio):.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^##\s+Original (Website Content|Content|Slack Content|Reddit Content|Blog Content|GitHub Content|Medium Content|Airtable Content)\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        if len(text) < 50:
            print(f"  Skipping {filename} (too short after cleaning)")
            continue

        source = filename.replace(".md", "").replace("_", " ").title()
        documents.append({
            "source": source,
            "filename": filename,
            "text": text,
            "year": year,
            "related_studio": related_studio,
        })

    print(f"Loaded {len(documents)} document(s).")
    return documents


def chunk_document(text, source, year="Unknown", related_studio="Unknown"):
    """
    Split a document into overlapping character-based chunks.

    Strategy:
      - Default chunk_size = 375 characters: fits 1–3 sentences or a short
        bullet list, carrying one complete idea without merging unrelated topics.
      - Awards documents use chunk_size = 600 characters: the Startup Awards
        articles describe each winner in a long bullet (~300-400 chars per
        company). At 375 chars, a single winner's name and description gets
        split across 2-3 chunks, each too fragmentary for retrieval to match.
        600 chars keeps one complete winner entry per chunk.
      - overlap = 75 characters for both: roughly one short sentence, enough
        to recover a boundary-spanning fact without excessive duplication.
      - min_length = 60 characters: filters whitespace artifacts and
        section headers with no body text.

    year and related_studio are stored as metadata on every chunk so that:
      - The LLM can surface the year when citing sources (important because
        the corpus spans 2018-2026 and some facts have changed over time).
      - Future metadata filtering (e.g., "only show 2026 documents") is
        possible without re-embedding.

    Returns a list of dicts with keys: text, source, year, related_studio, chunk_id.
    """
    # Awards articles have long per-winner bullet descriptions that get
    # fragmented at 375 chars — use a larger window for these documents.
    if "startup_awards" in source.lower().replace(" ", "_"):
        chunk_size = 600
    else:
        chunk_size = 375

    overlap = 75
    min_length = 60

    chunks = []
    prefix = source.lower().replace(" ", "_")
    counter = 0

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "source": source,
                "year": year,
                "related_studio": related_studio,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

        start += chunk_size - overlap

    return chunks