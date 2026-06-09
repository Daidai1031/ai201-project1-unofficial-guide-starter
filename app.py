import gradio as gr
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response

SOURCE_URLS = {
    "Official Product Studio": "https://tech.cornell.edu/studio/curriculum/product-studio/",
    "Official Startup Studio": "https://tech.cornell.edu/studio/curriculum/startup-studio/",
    "Official Bigco Studio": "https://tech.cornell.edu/studio/curriculum/bigco-studio/",
    "Official Pitech Impact Studio": "https://tech.cornell.edu/studio/curriculum/pitech-impact-studio/",
    "Official Studio Curriculum Overview": "https://tech.cornell.edu/studio/curriculum/",
    "Official Studio Josh Hartmann Interview": "https://tech.cornell.edu/news/studio-cornell-tech-josh-hartmann/",
    "Official Startup Awards 2025": "https://tech.cornell.edu/news/cornell-tech-startup-awards-2025/",
    "Official Startup Awards 2026": "https://tech.cornell.edu/news/2026-startup-awards-cornell-tech/",
    "Github Product Studio 2019": "https://github.com/cornelltech/product-studio",
    "Github Startup Studio 2019": "https://github.com/cornelltech/startup-studio",
    "Medium Startup Studio Reflection 2020": "https://medium.com/@hweelin.yeo/why-i-am-working-on-a-consumer-startup-at-cornell-tech-this-semester-ebdf49058969",
    "Medium Studio Constructive Criticism 2020": "https://medium.com/@yr49/6-reasons-why-the-studio-program-at-cornell-tech-succeeded-in-deserving-some-constructive-criticism-17cbbafaf57e",
    "Blog Bigco Studio Chad Dickerson 2018": "https://blog.chaddickerson.com/2018/10/18/bigco-studio/",
    "Reddit Studio Teams": "https://www.reddit.com/r/cornelltech_/comments/1kfjryo/studio_teams/",
}


def run_ingestion():
    collection = get_collection()
    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        return
    print("Ingesting Studio Guide documents...")
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"], doc["year"], doc["related_studio"])
        all_chunks.extend(chunks)
    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")


def handle_query(question):
    if not question.strip():
        return "", '<div class="src-box"><p class="src-label">Retrieved from</p><span class="src-empty">sources will appear here</span></div>'
    retrieved = retrieve(question)
    result = generate_response(question, retrieved)
    answer = result["answer"]
    items = ""
    for s in result["sources"]:
        key = s.split(" (")[0]
        url = SOURCE_URLS.get(key)
        if url:
            items += f'<a href="{url}" target="_blank" class="src-link">↗ {s}</a>'
        else:
            items += f'<span class="src-plain">◦ {s}</span>'
    if not items:
        items = '<span class="src-empty">No sources retrieved.</span>'
    sources_html = f'<div class="src-box"><p class="src-label">Retrieved from</p>{items}</div>'
    return answer, sources_html


CSS = """
/* ── Reset & page ─────────────────────────────────── */
.gradio-container {
    background: #f0f5f9 !important;
    min-height: 100vh;
    padding: 0 !important;
}
.gradio-container > .main > .wrap {
    padding: 0 !important;
    max-width: 100% !important;
}
footer { display: none !important; }

/* ── App shell ─────────────────────────────────────── */
#studio-app {
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px 20px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* ── Header ────────────────────────────────────────── */
#studio-header {
    text-align: center;
    padding-bottom: 20px;
    margin-bottom: 24px;
    border-bottom: 2px dashed #93c5fd;
}
#studio-header h1 {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 8px 0;
    letter-spacing: -0.3px;
}

/* ── Panels ─────────────────────────────────────────── */
.s-panel {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 0 !important;
    box-shadow: 4px 4px 0 #bfdbfe;
    padding: 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* ── Gradio textbox overrides ───────────────────────── */
#question-box textarea,
#answer-box textarea {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    background: #f8fafc !important;
    border-radius: 0 !important;
    color: #1e293b !important;
    resize: none !important;
}
#question-box textarea {
    font-size: 1rem !important;
    border: 1px solid #cbd5e1 !important;
    padding: 12px !important;
    line-height: 1.5 !important;
    margin-top: 6px !important;
}
#answer-box {
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    line-height: 1.7 !important;
    border: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
    padding: 14px !important;
    min-height: 390px;
    margin-top: 6px !important;
    color: #1e293b !important;
}
#answer-box p {
    margin: 0 0 12px 0 !important;
    color: #1e293b !important;
    font-weight: 400 !important;
}
#answer-box ul,
#answer-box ol {
    margin: 0 0 12px 18px !important;
    padding: 0 !important;
}
#answer-box li {
    margin-bottom: 8px !important;
    color: #1e293b !important;
    font-weight: 400 !important;
}
#answer-box strong {
    color: #0f172a !important;
    font-weight: 700 !important;
}

/* ── Label styling (White text on blue block) ───────── */
#question-box label span,
#answer-box label span {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #ffffff !important; /* 字体变成白色 */
    background-color: #0ea5e9 !important; /* 加上底色确保白色可见 */
    padding: 4px 8px !important;
    display: inline-block !important;
}

/* ── Example chips (Now Native Buttons) ─────────────── */
#chips-row {
    margin: 16px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: stretch;
}
.chips-label {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 2px;
}
.answer-label {
    display: inline-block;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
}
button.chip {
    font-size: 0.8rem !important;
    font-weight: normal !important;
    color: #0369a1 !important;
    background: #e0f2fe !important;
    border: 1px solid #bae6fd !important;
    border-radius: 0 !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    min-width: 0 !important;
    width: 100% !important;
    height: auto !important;
    justify-content: flex-start !important;
    text-align: left !important;
}
button.chip:hover { 
    background: #bae6fd !important; 
    color: #0c4a6e !important; 
    border-color: #7dd3fc !important;
}

/* ── Ask button ─────────────────────────────────────── */
#ask-btn button {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: bold !important;
    background: #0ea5e9 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: 3px 3px 0 #0284c7 !important;
    letter-spacing: 0.05em !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: all 0.1s ease !important;
    margin-top: auto; 
}
#ask-btn button:hover {
    box-shadow: 1px 1px 0 #0284c7 !important;
    transform: translate(2px, 2px) !important;
}
#ask-btn button:active {
    transform: translate(3px, 3px) !important;
    box-shadow: none !important;
}

/* ── Sources ────────────────────────────────────────── */
.src-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0;
    padding: 14px;
    min-height: 60px;
    margin-top: 16px;
}
.src-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    margin: 0 0 10px 0;
}
.src-link {
    display: block;
    font-size: 0.85rem;
    color: #0284c7;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    padding: 4px 0;
    width: fit-content;
}
.src-link:hover { 
    color: #0369a1; 
    border-bottom-color: #0369a1; 
}
.src-plain {
    display: block;
    font-size: 0.85rem;
    color: #64748b;
    padding: 4px 0;
}
.src-empty {
    font-size: 0.85rem;
    color: #94a3b8;
    font-style: italic;
}

#question-box,
#answer-box,
#question-box label,
#answer-box label {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#question-box label span,
#answer-box label span {
    color: #475569 !important;
    background: transparent !important;
    padding: 0 !important;
}
#question-box > *,
#question-box label,
#question-box div,
#question-box .wrap,
#question-box .container,
#question-box .form {
    background: transparent !important;
    box-shadow: none !important;
}
#question-box textarea {
    background: #f8fafc !important;
    color: #1e293b !important;
}
#answer-box {
    background: #ffffff !important;
}
"""

with gr.Blocks(css=CSS, title="Cornell Tech Studio Guide") as demo:

    with gr.Column(elem_id="studio-app"):

        gr.HTML("""
        <div id="studio-header">
            <h1>Cornell Tech Studio Guide</h1>
        </div>
        """)

        with gr.Row():
            
            # ── Input panel (左侧提问) ──────────────────────────────────────────
            with gr.Column(elem_classes=["s-panel"]):
                question_box = gr.Textbox(
                    label="Your question",
                    placeholder='e.g. "What are the team size requirements for Startup Studio?"',
                    lines=4,
                    elem_id="question-box",
                )

                with gr.Column(elem_id="chips-row"):
                    gr.HTML('<span class="chips-label">Try asking:</span>')
                    chip1 = gr.Button("Startup Studio team size?", elem_classes=["chip"])
                    chip2 = gr.Button("BigCo 2026 partners?", elem_classes=["chip"])
                    chip3 = gr.Button("2026 Award winners?", elem_classes=["chip"])
                    chip4 = gr.Button("Studio for founders?", elem_classes=["chip"])
                    chip5 = gr.Button("Student criticisms?", elem_classes=["chip"])

                ask_btn = gr.Button("→  Ask", elem_id="ask-btn")

            # ── Answer panel (右侧回答) ─────────────────────────────────────────
            with gr.Column(elem_classes=["s-panel"]):
                gr.HTML('<span class="answer-label">Answer</span>')
                answer_box = gr.Markdown(value="", elem_id="answer-box")

                sources_out = gr.HTML(
                    value='<div class="src-box"><p class="src-label">Retrieved from</p><span class="src-empty">sources will appear here after you ask a question</span></div>'
                )

    # 通过 Gradio 原生事件将点击映射为填入文本
    chip1.click(lambda: "Startup Studio team size requirements?", outputs=question_box)
    chip2.click(lambda: "What BigCo companies are partnering with Cornell Tech in 2026?", outputs=question_box)
    chip3.click(lambda: "Who won the 2026 Cornell Tech Startup Awards?", outputs=question_box)
    chip4.click(lambda: "I want to start my own company. Which Studio should I choose?", outputs=question_box)
    chip5.click(lambda: "What do students say are the weaknesses of the Studio program?", outputs=question_box)

    ask_btn.click(handle_query, inputs=question_box, outputs=[answer_box, sources_out])
    question_box.submit(handle_query, inputs=question_box, outputs=[answer_box, sources_out])


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  Cornell Tech Studio Guide — starting up")
    print("=" * 55 + "\n")
    run_ingestion()
    demo.launch()
