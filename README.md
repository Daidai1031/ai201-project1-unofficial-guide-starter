# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

### Cornell Tech Studio Guide

This project focuses on helping Cornell Tech students understand the Studio curriculum and choose between Product Studio, Startup Studio, BigCo Studio, and PiTech Impact Studio.

While Cornell Tech provides official course descriptions, students often struggle to understand what the Studio experience is actually like, how teams are formed, what types of projects students work on, how Startup Awards operate, and what partner companies or organizations expect from student teams.

Information about Studio is scattered across multiple sources, including official course pages, news, GitHub, Slack, blog posts, Reddit, and student reflections. Students often need to piece together information from many places to understand which Studio track best matches their interests and career goals.

The goal of this project is to create a searchable unofficial guide that consolidates these sources into a single retrieval system.

---


## Document Sources

| # | Source | Type | URL | File path |
|---|--------|------|-----|-----------|
| 1 | Product Studio | Official Website | https://tech.cornell.edu/studio/curriculum/product-studio/ | documents/official_product_studio.md |
| 2 | Startup Studio | Official Website | https://tech.cornell.edu/studio/curriculum/startup-studio/ | documents/official_startup_studio.md |
| 3 | BigCo Studio | Official Website | https://tech.cornell.edu/studio/curriculum/bigco-studio/ | documents/official_bigco_studio.md |
| 4 | PiTech Impact Studio | Official Website | https://tech.cornell.edu/studio/curriculum/pitech-impact-studio/ | documents/official_pitech_impact_studio.md |
| 5 | Studio Curriculum Overview | Official Website | https://tech.cornell.edu/studio/curriculum/ | documents/official_studio_curriculum_overview.md |
| 6 | Josh Hartmann Studio Interview | Official Website | https://tech.cornell.edu/news/studio-cornell-tech-josh-hartmann/ | documents/official_studio_josh_hartmann_interview.md |
| 7 | Startup Awards 2025 | Official Website | https://tech.cornell.edu/news/cornell-tech-startup-awards-2025/ | documents/official_startup_awards_2025.md |
| 8 | Startup Awards 2026 | Official Website | https://tech.cornell.edu/news/2026-startup-awards-cornell-tech/ | documents/official_startup_awards_2026.md |
| 9 | Product Studio Repository | GitHub | https://github.com/cornelltech/product-studio | documents/github_product_studio_2019.md |
| 10 | Startup Studio Repository | GitHub | https://github.com/cornelltech/startup-studio | documents/github_startup_studio_2019.md |
| 11 | Startup Studio Student Reflection | Medium | https://medium.com/%40hweelin.yeo/why-i-am-working-on-a-consumer-startup-at-cornell-tech-this-semester-ebdf49058969 | documents/medium_startup_studio_reflection_2020.md |
| 12 | Studio Program Constructive Criticism | Medium | https://medium.com/@yr49/6-reasons-why-the-studio-program-at-cornell-tech-succeeded-in-deserving-some-constructive-criticism-17cbbafaf57e | documents/medium_studio_constructive_criticism_2020.md |
| 13 | BigCo Studio Blog Post | Blog | https://blog.chaddickerson.com/2018/10/18/bigco-studio/ | documents/blog_bigco_studio_chad_dickerson_2018.md |
| 14 | Studio Teams Discussion | Reddit | https://www.reddit.com/r/cornelltech_/comments/1kfjryo/studio_teams/ | documents/reddit_studio_teams.md |
| 15 | Product Studio Pre-Work and Teaming | Slack | #product-studio-fall2023 | documents/slack_product_studio_prework_and_teaming.md |
| 16 | Startup Studio Team Formation | Slack | #startup-studio-spring2024 | documents/slack_startup_team_formation.md |
| 17 | Startup Studio Semester Activities | Slack | #startup-studio-spring2024 | documents/slack_startup_studio_semester_activities.md |
| 18 | BigCo Studio Matching Announcement | Slack | #bigco26 / #bigco26-teaming | documents/slack_bigco_studio.md |
| 19 | PiTech Partner Matching | Slack | #pitech-impact-sp26 | documents/slack_pitech_partner_matching.md |
| 20 | Google BigCo Partner Description | Airtable | [BigCo Studio 2026 Airtable record - Google](https://airtable.com/app9AQmQ8pSOcMc1Q/shrSgECZo21JkiP4b?sbe0w=recXmQIkacxIsCk1k) | documents/airtable_bigco_google_2026.md |
| 21 | IHG Hotels BigCo Partner Description | Airtable | [BigCo Studio 2026 Airtable record - IHG Hotels and Resorts](https://airtable.com/app9AQmQ8pSOcMc1Q/shrSgECZo21JkiP4b?sbe0w=rec0AF2RjvGB43JTE) | documents/airtable_bigco_ihg_hotels_2026.md |
| 22 | JPMorgan Chase BigCo Partner Description | Airtable | [BigCo Studio 2026 Airtable record - JPMorgan Chase](https://airtable.com/app9AQmQ8pSOcMc1Q/shrSgECZo21JkiP4b?sbe0w=recpjEpT6vaDzRNmf) | documents/airtable_bigco_jpmorgan_chase_2026.md |



---

## Chunking Strategy
 
**Chunk size:** 375 characters (600 characters for Startup Awards documents)
 
**Overlap:** 75 characters
 
**Why these choices fit your documents:**
 
The Studio Guide documents are a heterogeneous mix: structured prose paragraphs (official course pages, news articles), bullet-point lists (Slack announcements, GitHub FAQs), and narrative student reflections (Medium posts, Reddit comments). After skimming all 22 documents, key facts tend to appear in 1–3 sentence clusters.
 
375 characters fits roughly 1–3 sentences or a short bullet list — long enough to carry a complete idea without merging two unrelated topics. An initial test with 500 characters produced only 209 chunks across 22 documents and caused frequent mid-sentence breaks at chunk boundaries. Reducing to 375 raised the total to 293 chunks with cleaner boundaries.
 
The Startup Awards documents use a larger chunk size of 600 characters because each winner entry (name, description, founders) spans approximately 400–500 characters. At 375 characters, winner names were split across 2–3 fragments, each too short for retrieval to match "who won the awards" queries. Per-document chunk size logic in `chunk_document()` handles this automatically.
 
75 characters of overlap (20% of chunk size) ensures that a key fact landing exactly on a chunk boundary still appears in full in at least one chunk. A smaller overlap of 50 characters risks cutting mid-sentence; overlap above 100 characters causes adjacent chunks to be too semantically similar, degrading retrieval by returning near-duplicate results.
 
**Final chunk count:** 273 chunks across 22 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2`

**Production tradeoff reflection:**

**Production tradeoff reflection:**
 
For a real deployment serving Cornell Tech students at scale, I would weigh several tradeoffs:
 
- **Context length:** `all-MiniLM-L6-v2` truncates input at 256 tokens (~200 words). Several Studio documents — especially the Startup Awards articles and Slack digests — contain passages longer than this. A model with a higher context limit, such as OpenAI's `text-embedding-3-large` (8,191 tokens), would embed those documents more faithfully without truncation.
- **Accuracy on domain-specific text:** The Studio corpus contains proper nouns (Dreamteam, Maker Day, Startup Awards, PiTech) that a general-purpose model like MiniLM may not represent as precisely as a fine-tuned academic or enterprise model. A domain-adapted model would likely improve retrieval on track-specific queries.
- **Latency and cost:** `all-MiniLM-L6-v2` runs locally with zero network latency. An API-hosted model like `text-embedding-3-large` would add 50–200ms per query and incur per-token costs — acceptable for low-traffic internal tools, significant at scale.
- **Multilingual support:** Not a concern for this English-only corpus, but relevant if the system were extended to serve international students writing queries in other languages.
  
---

## Grounded Generation
 
**System prompt grounding instruction:**
 
Grounding is enforced through a six-rule system prompt passed to `llama-3.3-70b-versatile` via Groq. The critical rules are:
 
> "Answer ONLY using information explicitly stated in the provided context documents. Do NOT use any general knowledge about Cornell Tech, universities, or startups that is not in the context."
 
> "If the context contains no relevant information at all, respond with: 'The Studio Guide documents I have don't contain enough information to answer that. You may want to check the Cornell Tech website directly or ask a current student.'"
 
> "If the context does not contain direct information about the specific Studio track the user asked about, do NOT silently substitute information from a different track. First explicitly acknowledge the gap, then offer related information from another track only with a clear caveat."
 
The system prompt also instructs the model to cite sources using `[Source N: name (year)]` labels injected into each chunk's context block, and to flag temporal conflicts when a 2019 document and a 2026 document say different things.
 
In addition, chunks with cosine distance above 0.6 are filtered out before the context block is built, preventing weak matches from misleading the model.
 
**How source attribution is surfaced in the response:**
 
Source attribution operates at two levels. First, the LLM cites `[Source N]` labels inline in its answer. Second, `generate_response()` builds a deduplicated sources list programmatically from chunk metadata — independent of what the LLM writes — and returns it as a separate `sources` field. The Gradio UI displays this list in a "Retrieved from" panel below the answer, with clickable hyperlinks for documents that have public URLs (Cornell Tech pages, GitHub, Medium, Reddit, the Chad Dickerson blog). Slack and Airtable sources, which have no public URL, appear as plain text citations.
 
This two-level approach guarantees attribution even if the model fails to cite sources inline, and ensures the sources panel reflects what was actually retrieved rather than what the LLM hallucinated.
 
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

## Evaluation Report
 
| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the team size requirements for Startup Studio? | 4 students/2 programs or 5 students/3 programs; 3-person exception requires Josh's approval. | Correctly stated both size options and the exception rule, cited Slack Startup Team Formation 2026. | Relevant | Accurate |
| 2 | What BigCo companies are partnering with Cornell Tech in 2026? | Seven companies: Catholic Health, CSL Behring, Google, IHG Hotels, JPMorgan Chase, Samsung, TikTok. | Failed to list the 7 companies despite Slack BigCo Studio chunk (dist: 0.41) containing the full list. LLM noted only that "Google and JPMorgan Chase are mentioned as examples." Directed user to Cornell Tech website. | Partially relevant | Inaccurate |
| 3 | Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive? | Aiseptor, Custos, Kindred, Lola ($100K each); CoagHealth and MedComm as runner-ups (Runway). | Correctly stated $100K per team and described four AI project categories, but named no winning companies. Listed finalist teams instead (Daunt, Ephemeris, NYX Labs). | Relevant | Partially accurate |
| 4 | I want to start my own company after graduation. Which Studio track should I choose and why? | Startup Studio (primary); PiTech for public interest; BigCo Studio not for independent founding. | Recommended Startup Studio with Startup Award details, contrasted with BigCo Studio. Did not mention PiTech as an alternative — not in top-5 retrieved chunks. | Partially relevant | Partially accurate |
| 5 | What do students say are the weaknesses of the Studio program? | Six criticisms from 2020 Medium post: passion, experience, nepotism, guest speakers, grading, accountability. | Covered faculty passion, grading standards, and nepotism correctly. Source 3 (Chad Dickerson blog, positive content) was retrieved and cited despite being irrelevant to weaknesses. | Partially relevant | Partially accurate |
| 6 | What is the weekly class schedule and structure of PiTech Impact Studio? | Documents don't contain a weekly schedule; system should acknowledge gap without fabricating. | Correctly acknowledged no direct PiTech schedule information. Offered Startup Studio 2019 schedule as reference with explicit caveat. Did not fabricate PiTech-specific content. | Off-target (by design) | Accurate (correct refusal) |
 

---
## Failure Case Analysis
 
**Failure Case 1 — Year disambiguation failure (fixed)**
 
**Question that failed:** Who won the 2026 Cornell Tech Startup Awards?
 
**What the system returned (before fix):** The top two retrieved chunks both came from the 2025 Startup Awards document (distances 0.316 and 0.324), ranking higher than the correct 2026 document (distance 0.361). A language model given this context could easily confuse the 2025 winners (CreditQuant AI, gymii.ai, Polyrook, SAIL) for the 2026 winners (Aiseptor, Custos, Kindred, Lola).
 
**Root cause (tied to a specific pipeline stage):** Retrieval-stage failure caused by the embedding model (`all-MiniLM-L6-v2`). The 2025 and 2026 Startup Awards articles have nearly identical sentence structure — both describe "four student teams," "$100,000 investments," and "Startup Studio." The semantic vectors for the two documents are very similar, so cosine distance cannot distinguish them by year token alone.
 
**Fix applied:** Added automatic year metadata filtering in `retrieve()`. When a query contains a 4-digit year (detected via regex), ChromaDB applies `where={"year": {"$eq": "2026"}}` before semantic ranking. After the fix, all 5 returned chunks came from the 2026 document.
 
---
 
**Failure Case 2 — Cross-track contamination and ChromaDB API limitation**
 
**Question that failed:** How does team formation work in Product Studio?
 
**What the system returned:** Result 4 came from Official Startup Studio 2026 (describing Startup Studio's self-organized teaming), and Result 5 came from a 2020 Medium post criticizing faculty nepotism. Only 3 of 5 chunks directly addressed Product Studio team formation.
 
**Root cause (tied to two pipeline stages):** First, a retrieval-stage failure: "team formation" is semantically broad and matches any Studio track. Second, a deeper infrastructure limitation: `retrieve()` was designed to apply `{"related_studio": {"$contains": "Product Studio"}}` when the query names a specific track. However, ChromaDB's `$contains` operator does not support string metadata fields. The Reddit Studio Teams document stores `related_studio` as `"Product Studio / Startup Studio / BigCo Studio"` (slash-separated, since ChromaDB metadata cannot store lists), so the filter returned 0 results and fell back to full-corpus search.
 
**What you would change to fix it:** Apply track filtering as a Python post-processing step — retrieve top-10 candidates, filter in Python using `any(track in chunk["related_studio"] for track in ["Product Studio"])`, then return the top-5. This sidesteps ChromaDB's API limitation entirely.
 
---
 
**Failure Case 3 — LLM ignores relevant chunk content (Q2 and Q3)**
 
**Question that failed (Q2):** What BigCo companies are partnering with Cornell Tech in 2026?
 
**What the system returned:** Retrieved Result 3 was `Slack Bigco Studio (2026)` at distance 0.41, and its text contained the complete list: "This year, BigCo Studio is partnering with seven organizations: Catholic Health, CSL Behring, Google, IHG Hotels, JPMorgan Chase, Samsung, TikTok." Despite this chunk being in the context, the LLM responded that it could not find specific company names and directed the user to the Cornell Tech website.
 
**Root cause (tied to a specific pipeline stage):** This is a generation-stage failure, not a retrieval failure. The relevant chunk was successfully retrieved (dist: 0.41, well below the 0.6 threshold). The failure occurred because the LLM weighted higher-ranked chunks (Results 1 and 2, with lower distances) more heavily in its response, and those chunks described BigCo Studio's structure rather than listing partner names. When the answer is buried in a lower-ranked chunk, the model tends to synthesize from the most semantically prominent content rather than scanning all five chunks equally.
 
The same pattern explains Q3: winner names appeared in Chunks 4–5 (dist: 0.42–0.43), but the LLM summarized from the higher-ranked Chunks 1–2 (dist: 0.30–0.31), which described the awards event and funding amounts without naming companies.
 
**What you would change to fix it:** Two options. First, instruct the model in the system prompt to explicitly scan all provided chunks before answering, not just rely on the most prominent ones: "Read all context documents carefully before answering. Do not skip lower-ranked sources." Second, increase n_results from 5 to 8 for queries that involve lists or enumerations, giving the model more surface area to find specific names. A reranking step that specifically promotes chunks containing named entities would also help.
 
---
 
## Spec Reflection
 
**One way the spec helped you during implementation:**
 
The planning.md Anticipated Challenges section proved directly useful during Milestone 4. Writing the challenge about sparse PiTech coverage before implementation forced a concrete decision: the system prompt must explicitly instruct the LLM to acknowledge when it lacks direct information about a specific track, rather than silently substituting content from another track. When PiTech retrieval returned Startup Studio schedule chunks during testing, the LLM correctly said "The documents I have don't contain direct information about PiTech Impact Studio on this topic" and offered the Startup Studio schedule only with an explicit caveat — exactly the behavior the spec had anticipated and designed for.
 
**One way your implementation diverged from the spec, and why:**
 
The spec described a uniform chunk size of 375 characters for all documents. During Milestone 5 evaluation, the system consistently failed to name the 2026 Startup Award winners despite retrieving the correct document — a failure traced to chunk fragmentation in the awards articles. Each winner's description spans 400–500 characters, larger than a single 375-char chunk, causing names to appear in fragments with weak semantic signal. The fix introduced per-document chunk size logic: awards documents use 600 characters while all others retain 375. This divergence from the spec was driven by an empirical failure discovered during evaluation, not a design change made in advance — which is exactly why evaluation matters.
 
---
 
## AI Usage
 
**Instance 1 — Retrieval failure diagnosis and metadata filtering fix**
 
*What I gave the AI:* The full terminal output from `tests/test_retriever.py` showing two failure patterns: (1) the 2025 Startup Awards document outranking the 2026 document on the query "Who won the 2026 Cornell Tech Startup Awards?", with distances 0.316 and 0.324 for the wrong-year chunks versus 0.361 for the correct one; and (2) Startup Studio and unrelated Medium content appearing in results for "How does team formation work in Product Studio?" I described both problems and asked Claude to explain the root cause and propose a fix.
 
*What it produced:* Claude identified that the year disambiguation failure was caused by the embedding model treating structurally identical articles as semantically equivalent, unable to weight a year token more heavily than surrounding prose. It proposed adding automatic metadata filtering in `retrieve()`: detecting a 4-digit year via regex and passing `where={"year": {"$eq": "2026"}}` to ChromaDB. For cross-track contamination, it proposed a `$contains` filter on `related_studio`. It produced the full updated `retriever.py` with a `_build_where_filter()` helper and a fallback to full-corpus search when the filter returns 0 results.
 
*What I changed or overrode:* The year filtering fix worked exactly as proposed. However, I noticed the `$contains` track filter was silently failing for all track-specific queries. Investigating the output, I found that ChromaDB's `$contains` operator does not support string metadata fields — it only works on array types. The Reddit Studio Teams document stores `related_studio` as a slash-separated string, which `$contains` cannot match. I documented this as Failure Case 2 in the README rather than attempting a more complex workaround, since it represents a real infrastructure limitation worth explaining honestly.
 
---
 
**Instance 2 — Chunk fragmentation diagnosis and per-document chunk size fix**
 
*What I gave the AI:* The terminal output from `tests/test_generator.py` showing that the system returned the correct $100,000 funding amount for the 2026 Startup Awards but could not name any of the winners. I described that the issue persisted even with k=8, and shared the output of `tests/debug_awards.py` showing the 2026 awards document produced 19 chunks at 375 characters, with winner names distributed across Chunks 4–10 — none of which ranked in the top-8 retrieved results. I asked Claude to explain why and propose a targeted fix that would not affect other documents.
 
*What it produced:* Claude identified that 375-character chunking fragmented each winner's entry (name + description + founders, ~400–500 chars) across 2–3 chunks, each too short to carry enough semantic signal. It proposed a conditional inside `chunk_document()`: if the source name contains `"startup_awards"`, use `chunk_size=600`; otherwise use 375. It produced the updated function with the conditional and a docstring explaining the per-document rationale.
 
*What I changed or overrode:* The fix was applied as proposed. I deleted `chroma_db/` and re-ingested all documents to rebuild the vector store with the new chunk sizes. I verified using `tests/debug_awards.py` that the awards document now produced 11 chunks (down from 19) with winner names in Chunks 2–5 at 599–600 characters each. Running `tests/debug_awards_k8.py` confirmed that winner-name chunks now ranked within the top-5 for this query.
 