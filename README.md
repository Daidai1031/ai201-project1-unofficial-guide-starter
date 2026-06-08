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

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

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

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
