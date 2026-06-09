# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Cornell Tech's Studio program is a required curriculum component for all master's students, but the official website only provides polished, high-level descriptions of each track. Students who want to understand what Studio is actually like, for example how teams form, what Startup Awards look like in practice, what BigCo partner companies expect, what past students thought worked and didn't, have to piece that together from scattered sources: Slack, Reddit, Medium, GitHub, and news articles.

This project consolidates those sources into a single searchable system. The knowledge is valuable because it directly affects student's decision-make even the future career path.

---

## Documents


| # | Source    | Type      | URL | File path |
|---|-----------|-----------|-----|-----------|
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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 75 characters

**Why these choices fit your documents:**

The Studio Guide documents are a heterogeneous mix: some are structured prose paragraphs (official course pages, news articles), some are bullet-point lists (Slack, GitHub), and some are narrative student reflections (Medium posts, Reddit comments). After skimming all 22 documents, the key facts tend to appear in 2–4 sentence clusters.
 
500 characters fits roughly 2–4 sentences or a short bullet list, which is long enough to carry a complete idea without merging two unrelated topics into the same chunk. A smaller size like 200 characters would fragment multi-sentence explanations; a larger size characters would blend unrelated sections.
 
75 characters of overlap ensures that a key fact landing exactly on a chunk boundary (which character-based splitting makes likely) still appears in full in at least one chunk. 75 characters is roughly one short sentence, which is enough to recover context without significantly duplicating content across the database.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 5

Retrieving 5 chunks gives the LLM enough cross-source context without flooding it with loosely related material. In testing, retrieving 3 was sometimes too narrow for multi-faceted questions; retrieving 8 occasionally introduced off-topic chunks that distracted the model.

**Production tradeoff reflection:**

- **Latency and cost:** `all-MiniLM-L6-v2` runs locally with zero latency from network calls. An API-hosted model like OpenAI's `text-embedding-3-large` would add ~50–200ms per query and incur per-token costs, which matter at scale.
- **Context length:** `all-MiniLM-L6-v2` embeds up to 256 tokens. Some Studio documents (especially the Startup Awards articles and Slack digests) contain passages longer than this. A model with a higher context limit, such as `text-embedding-3-large` (8191 tokens), would embed those documents more faithfully.\

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the team size requirements for Startup Studio? | 4 students from at least 2 degree programs, or 5 students from at least 3 degree programs. A 3-person exception requires explicit approval from Josh Hartmann. |
| 2 | What BigCo companies are partnering with Cornell Tech in 2026? | Seven companies: Catholic Health, CSL Behring, Google, IHG Hotels, JPMorgan Chase, Samsung, and TikTok. |
| 3 | Who won the 2026 Cornell Tech Startup Awards and how much funding did they receive? | Four teams each received $100,000: Aiseptor, Custos, Kindred, and Lola. Two runner-ups (CoagHealth and MedComm) received office space and mentorship through Runway but no cash. |
| 4 | I want to start my own company after graduation. Which Studio track should I choose and why? | Startup Studio is the primary track for aspiring founders, with the option to apply for a $100,000 Startup Award. PiTech is an alternative for public-interest startups. BigCo Studio is not designed for founding a company. |
| 5 | What do students say are the weaknesses of the Studio program? | A 2020 Medium post cited six criticisms: faculty lacking passion, insufficient teaching experience, nepotism in hiring, repetitive guest speakers, unclear grading standards, and lack of accountability. |
| 6 | What is the weekly class schedule and structure of PiTech Impact Studio? | The documents do not contain a detailed weekly schedule. The system should acknowledge this gap rather than fabricating a schedule. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Uneven document coverage across Studio tracks causing cross-track substitution:** The corpus has strong coverage of Product Studio (GitHub FAQ, Slack pre-work, official page) and Startup Studio (Slack teaming, semester activities, multiple Medium reflections), but much thinner coverage of PiTech Impact Studio. When a user asks a PiTech-specific question (e.g., "What is the weekly schedule like in PiTech Studio?"), the top-5 retrieved chunks may include less than 5 PiTech documents and instead surface structurally similar content from Startup Studio or BigCo Studio. The LLM could then misattribute that information to PiTech, producing a confident-sounding but incorrect answer. The mitigation is twofold: the system prompt instructs the model to explicitly acknowledge when it cannot find direct information about the queried track, and to offer related information from other tracks only with a clear explanation, for example, "The documents I have don't contain specific information about PiTech's weekly schedule, but Startup Studio's schedule (which runs in the same semester) looks like this: ..."

2. **Temporal inconsistency across documents:** The corpus spans 2018–2026. Some details have changed over time — for example, the GitHub 2019 docs describe a different team size than the 2026 Slack announcements. If a user asks "How big are Product Studio teams?", the retriever may surface both old and new information. The generator must be prompted to prefer more recent sources and to note discrepancies when they exist, but not to give the specific date precisely.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```
    user query
        │
        ▼
[1] INGESTION — ingest.py
    load_documents(): reads .md files, light cleaning (image syntax, collapse whitespace)
    chunk_document(): character-based sliding window, 500 chars, 75 overlap

        │
        ▼
[2] EMBEDDING + VECTOR STORE — retriever.py
    embed_and_store(): sentence-transformers all-MiniLM-L6-v2 → ChromaDB (cosine)
    Persistent store: ./chroma_db
        │
        ▼
[3] RETRIEVAL — retriever.py
    retrieve(): ChromaDB semantic search, top-5 results with source metadata + distance
        │
        ▼
[4] GENERATION — generator.py
    generate_response(): Groq llama-3.3-70b-versatile
    Grounding: system prompt forbids answers outside retrieved context
    Attribution: chunks labeled [Source N: filename] in context block
        │
        ▼
[5] UI — app.py
    Gradio Chat Interface
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

I will use claude to generate `ingest.py` according to `planning.md`, with 500-character chunks and 75-character overlap. I will verify the output by printing 5 random chunks and checking that each is readable and self-contained.


**Milestone 4 — Embedding and retrieval:**

I will give Claude the Retrieval Approach section of this planning.md, and ask it to genrate `retriever.py`. I will specify that the return format must include text, source, and distance fields. I will verify by running 3 of my evaluation plan queries manually and checking that returned chunks visibly relate to each question.

**Milestone 5 — Generation and interface:**

I will give Claude the Anticipated Challenges section, my system prompt requirements (no outside knowledge, cite sources by label, explicit fallback message), and ask it to generate `generator.py`. I will test grounding by asking a question my documents don't cover and verifying the system declines to speculate. I will also ask Claude to generate Gradio UI to fit the Studio Guide domain.