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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 75 characters

**Why these choices fit your documents:**

The Studio Guide documents are a heterogeneous mix: some are structured prose paragraphs (official course pages, news articles), some are bullet-point lists (Slack, GitHub), and some are narrative student reflections (Medium posts, Reddit comments). After skimming all 22 documents, the key facts tend to appear in 2–4 sentence clusters.
 
500 characters fits roughly 2–4 sentences or a short bullet list, which is long enough to carry a complete idea without merging two unrelated topics into the same chunk. 

75 characters is roughly one short sentence, which is enough to recover context without significantly duplicating content across the database.

**Final chunk count:** 

**Chunk size:** 375 characters
 
**Overlap:** 75 characters

**Reasoning:**

When I tested ingest with `tests/test_ingest.py`, I notice that some of the output chunks are included with multi-topics, which means will be too diluted to match any specific query. At same time, the totol chunks is only 209, which is too small for 22 documents. So I changed chunk count to 375，the final totol chunkss is 293.

375 characters fits roughly 1–3 sentences or a short bullet list, which is long enough to carry a complete idea without merging two unrelated topics into the same chunk. A smaller size like 200 characters would fragment multi-sentence explanations; a larger size like 500 characters frequently merges unrelated paragraphs and causes chunk boundaries to fall mid-sentence, producing fragments at chunk openings that reduce retrieval precision.
 
I keep 75 characters of overlap (20% of chunk size), ensuring that a key fact landing exactly on a chunk boundary still appears in full in at least one chunk. A smaller overlap of 50 characters risks cutting mid-sentence on boundary-spanning facts; a larger overlap of 100+ characters causes adjacent chunks to be too semantically similar, which degrades retrieval by returning near-duplicate results.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2`

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

## Evaluation Report
 
| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the team size requirements for Startup Studio? | 4 students from at least 2 degree programs, or 5 students from at least 3 degree programs. A 3-person exception requires explicit approval from Josh Hartmann. | | | |
| 2 | What BigCo companies are partnering with Cornell Tech in 2026? | Seven companies: Catholic Health, CSL Behring, Google, IHG Hotels, JPMorgan Chase, Samsung, and TikTok. Source is a 2026 Slack announcement from the BigCo Studio teaming channel. | | | |
| 3 | Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive? | Four teams each received $100,000: Aiseptor (AI exam fraud prevention), Custos (programmable AI payment policies), Kindred (medical device regulation AI), and Lola (institutional knowledge automation). Two runner-ups — CoagHealth and MedComm — received office space and mentorship through Runway but no cash investment. | | | |
| 4 | I want to start my own company after graduation. Which Studio track should I choose and why? | Startup Studio is the primary track for aspiring founders: students develop their own product idea, pitch to investors, and can apply for a $100,000 Startup Award plus one year of free co-working space. PiTech Impact Studio is an alternative if the startup focuses on public interest or underserved communities. BigCo Studio is designed for innovating within large organizations, not for founding an independent company. | | | |
| 5 | What do students say are the weaknesses of the Studio program? | A 2020 Medium post by a Cornell Tech student cited six criticisms: faculty lacking passion for teaching, insufficient teaching experience among Studio team members, nepotism in faculty hiring (many worked together previously), repetitive guest speakers, unclear and subjective grading standards, and a general lack of accountability in the program. | | | |
| 6 | What is the weekly class schedule and structure of PiTech Impact Studio? | The loaded documents do not contain a detailed weekly schedule for PiTech Impact Studio. What is available: the course runs in spring semester for 3 credits, taught by Matthew Klein and Ariel Kennan, and involves weekly lectures, fireside chats, and Crit/Maker Days. The system should acknowledge the gap and not fabricate a schedule. | | | |
 

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Failure Case 1 — Year disambiguation failure**
 
**Question that failed:** Who won the 2026 Cornell Tech Startup Awards?
 
**What the system returned:** The top two retrieved chunks both came from the *2025* Startup Awards document (distances 0.316 and 0.324), ranking higher than the correct 2026 document (distance 0.361). The 2026 winners (Aiseptor, Custos, Kindred, Lola) appeared only in Result 3 and Result 5. A language model given this context could easily confuse the 2025 winners (CreditQuant AI, gymii.ai, Polyrook, SAIL) for the 2026 winners, since both sets of chunks appear in the retrieved set without clear ranking priority by year.
 
**Root cause (tied to a specific pipeline stage):** This is a retrieval-stage failure caused by the embedding model (`all-MiniLM-L6-v2`). The 2025 and 2026 Startup Awards articles have nearly identical sentence structure — both describe "four student teams," "$100,000 investments," "Startup Studio," and "Cornell Tech." The semantic vectors for these two documents are very similar, so cosine distance cannot distinguish between them based on the year token alone. The embedding model has no mechanism to weight a specific number ("2026") more heavily than the surrounding prose.
 
**What you would change to fix it:** Two options. First, metadata filtering: since `year` is stored as metadata on every chunk, a query explicitly mentioning a year (e.g. "2026") could trigger a `where={"year": "2026"}` filter in ChromaDB before semantic search runs, restricting results to 2026 documents only. Second, a reranking step: after retrieval, a cross-encoder reranker could re-score chunks by comparing the full query text against each chunk more precisely, down-ranking the 2025 chunks. The metadata filter approach is simpler and would directly solve this case.
 
---
 
**Failure Case 2 — Cross-track contamination and ChromaDB API limitation**
 
**Question that failed:** How does team formation work in Product Studio?
 
**What the system returned:** Result 4 came from *Official Startup Studio 2026* (describing Startup Studio's self-organized teaming process), and Result 5 came from a 2020 Medium post criticizing faculty nepotism — unrelated to Product Studio team formation. Only 3 of 5 chunks directly addressed the question.
 
**Root cause (tied to two pipeline stages):**
 
First, a retrieval-stage failure: the query "team formation" is semantically broad and matches any Studio track that involves forming teams. The embedding model cannot infer that the user specifically wants Product Studio content.
 
Second, a deeper infrastructure limitation discovered during the fix attempt: the fix designed `retrieve()` to apply a `{"related_studio": {"$contains": "Product Studio"}}` filter in ChromaDB when the query names a specific track. This correctly handles single-value fields like `"Product Studio"`, but ChromaDB's `$contains` operator does not support string metadata fields — it only works on array types. One document (`Reddit Studio Teams`) stores `related_studio` as `"Product Studio / Startup Studio / BigCo Studio"` (a slash-separated string, since ChromaDB metadata cannot store lists). The filter returned 0 results and fell back to full-corpus search, leaving the cross-track contamination unfixed for this query.
 
**What you would change to fix it:** Two options. First, apply track filtering as a Python post-processing step after retrieval rather than inside ChromaDB — retrieve more candidates (e.g. top-10), then filter in Python using `any(track in chunk["related_studio"] for track in ["Product Studio"])`, then return the top-5 of the filtered set. This sidesteps ChromaDB's API limitation entirely. Second, at ingestion time, duplicate chunks from multi-track documents into separate records per track, so each chunk has a single-value `related_studio` field that `$eq` can match precisely.

**Failure Case 3 — Chunk fragmentation causes winner names to be unretrievable (fixed)**
 
**Question that failed:** Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive?
 
**What the system returned (before fix):** The system correctly stated that four teams each received $100,000, but could not name any of the winners (Aiseptor, Custos, Kindred, Lola) or runner-ups (CoagHealth, MedComm). Even with k=8, the answer described winning projects only by category — "blocks AI exam fraud," "makes financial AI transactions safer" — with no company names.
 
**Root cause (tied to a specific pipeline stage):** This is an ingestion/chunking-stage failure. The 2026 Startup Awards article produced 19 chunks at 375 characters each. Winner names and descriptions are spread across Chunks 4–10, but each chunk contains only a fragment of one winner's entry — for example, one chunk starts mid-sentence ("instead of trying to catch cheating after it happens...") and another contains only a founder name list with no company name attached. When embedded, these fragments carry weak semantic signal for the query "who won the awards." All name-containing chunks ranked below distance 0.5, outside the top-8 retrieved results. The year filter correctly restricted results to 2026 documents, but could not compensate for the fragmentation within those documents.
 
**Fix applied:** Added per-document chunk size logic in `chunk_document()`. Documents whose source name contains `"startup_awards"` now use `chunk_size=600` instead of 375. At 600 characters, each winner's name, description, and founders fit within a single chunk, giving the embedding enough semantic context to match "who won" queries. All other documents retain the 375-character default. After re-ingesting with the fix, the awards chunks containing winner names rank in the top-5 for this query.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
  the output from terminal, decribe the problem(Year disambiguation failure, ), ask ai how to fix it.
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
