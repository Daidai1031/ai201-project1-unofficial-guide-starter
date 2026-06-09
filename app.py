import re
import gradio as gr
from ingest import load_documents, chunk_document
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response


def render_bold(text):
    """Convert **bold** to explicit <strong> so it renders even when the
    bold span sits directly next to CJK characters (e.g. **A**和**B**),
    which Markdown's flanking-delimiter rules otherwise fail to parse."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

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
    answer = render_bold(result["answer"])
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


GREETING = (
    "Hi! I'm your Cornell Tech **Studio Guide**. Ask me anything about the Studio "
    "program — team sizes, BigCo partners, award winners, or which Studio fits your "
    "goals. Pick a suggestion on the left or type your own question."
)


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-top:    #e8eef8;
    --bg-bottom: #f5f8fc;
    --card:      #ffffff;
    --border:    #e4e9f2;
    --ink:       #1e293b;
    --ink-strong:#0f172a;
    --muted:     #64748b;
    --accent:      #2563eb;
    --accent-deep: #1d4ed8;
    --accent-soft: #eef4ff;
    --ring:        rgba(37, 99, 235, 0.16);
    --font: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* -- Force a light appearance, even in OS/browser dark mode -- */
.gradio-container,
.gradio-container.dark,
.dark,
.dark .gradio-container {
    --body-background-fill: transparent;
    --background-fill-primary: transparent;
    --background-fill-secondary: transparent;
    --block-background-fill: transparent;
    --block-border-color: transparent;
    --panel-background-fill: transparent;
    --input-background-fill: #f8fafc;
    --border-color-primary: var(--border);
    --body-text-color: var(--ink);
    --body-text-color-subdued: var(--muted);
    color: var(--ink) !important;
}

/* -- Page -------------------------------------------- */
.gradio-container {
    background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 55%) !important;
    min-height: 100vh;
    padding: 0 !important;
    font-family: var(--font) !important;
}
.gradio-container > .main > .wrap {
    padding: 0 !important;
    max-width: 100% !important;
}
footer { display: none !important; }

/* -- App shell --------------------------------------- */
#studio-app {
    max-width: 1060px;
    margin: 0 auto;
    padding: 42px 22px 56px;
    font-family: var(--font);
}

/* -- Header ------------------------------------------ */
#studio-header { text-align: center; margin-bottom: 30px; }
#studio-header .logo {
    width: 48px; height: 48px;
    margin: 0 auto 14px;
    border-radius: 15px;
    background: linear-gradient(135deg, #2563eb, #4f8cff);
    color: #fff;
    font-size: 1.25rem;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.32);
}
#studio-header h1 {
    font-family: var(--font);
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--ink-strong);
    margin: 0;
    letter-spacing: -0.4px;
}
#studio-header p {
    margin: 8px 0 0;
    font-size: 0.95rem;
    color: var(--muted);
}

/* -- Panels (cards) ---------------------------------- */
#studio-app .s-panel,
.s-panel {
    background: var(--card) !important;
    border: 1px solid var(--border);
    border-radius: 18px !important;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.07);
    padding: 22px !important;
    height: 100%;
    display: flex;
    flex-direction: column;
}

/* -- Question textbox -------------------------------- */
#question-box textarea {
    font-family: var(--font) !important;
    font-size: 0.98rem !important;
    background: #f8fafc !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--ink) !important;
    padding: 14px !important;
    line-height: 1.55 !important;
    resize: none !important;
    margin-top: 8px !important;
    transition: border-color .15s ease, box-shadow .15s ease !important;
}
#question-box textarea::placeholder { color: #94a3b8 !important; }
#question-box textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--ring) !important;
}

/* -- Field labels ------------------------------------ */
#question-box label span {
    font-family: var(--font) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
    background: transparent !important;
    padding: 0 !important;
}

/* -- Answer header (chat style) ---------------------- */
.answer-head {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 14px;
}
.answer-head .avatar {
    width: 36px; height: 36px;
    flex: none;
    border-radius: 11px;
    background: linear-gradient(135deg, #2563eb, #4f8cff);
    color: #fff;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 5px 14px rgba(37, 99, 235, 0.28);
}
.answer-head .answer-name {
    display: block;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink-strong);
    line-height: 1.15;
}
.answer-head .answer-sub {
    display: block;
    font-size: 0.72rem;
    color: var(--muted);
}

/* -- Answer body ------------------------------------- */
#answer-box {
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    line-height: 1.72 !important;
    border: 1px solid var(--border) !important;
    background: #fbfcfe !important;
    border-radius: 12px !important;
    padding: 16px 18px !important;
    min-height: 320px;
    color: var(--ink) !important;
}
#answer-box p {
    margin: 0 0 12px 0 !important;
    color: var(--ink) !important;
}
#answer-box p:last-child { margin-bottom: 0 !important; }
#answer-box ul,
#answer-box ol {
    margin: 0 0 12px 18px !important;
    padding: 0 !important;
}
#answer-box li {
    margin-bottom: 6px !important;
    color: var(--ink) !important;
}
#answer-box strong {
    color: var(--ink-strong) !important;
    font-weight: 600 !important;
}

/* -- Suggestion chips (pills) ------------------------ */
#chips-row {
    margin: 18px 0 4px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.chips-label {
    flex-basis: 100%;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 4px;
}
button.chip {
    font-family: var(--font) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--accent-deep) !important;
    background: var(--accent-soft) !important;
    border: 1px solid #dbe6ff !important;
    border-radius: 999px !important;
    padding: 7px 14px !important;
    cursor: pointer !important;
    transition: all .15s ease !important;
    box-shadow: none !important;
    width: auto !important;
    min-width: 0 !important;
    flex: 0 0 auto !important;
    height: auto !important;
}
button.chip:hover {
    background: #dde9ff !important;
    border-color: #b9d0ff !important;
    transform: translateY(-1px);
}

/* -- Ask button -------------------------------------- */
#ask-btn {
    margin-top: auto;
    padding-top: 18px;
}
#ask-btn button {
    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.30) !important;
    letter-spacing: 0.02em !important;
    padding: 12px 20px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: transform .12s ease, box-shadow .12s ease !important;
}
#ask-btn button:hover {
    transform: translateY(-1px);
    box-shadow: 0 11px 24px rgba(37, 99, 235, 0.38) !important;
}
#ask-btn button:active {
    transform: translateY(0);
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.30) !important;
}

/* -- Sources ----------------------------------------- */
.src-box {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 16px;
}
.src-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin: 0 0 10px 0;
}
.src-link {
    display: block;
    font-size: 0.85rem;
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    padding: 5px 0;
    width: fit-content;
    transition: color .15s ease, border-color .15s ease;
}
.src-link:hover {
    color: var(--accent-deep);
    border-bottom-color: var(--accent-deep);
}
.src-plain {
    display: block;
    font-size: 0.85rem;
    color: var(--muted);
    padding: 5px 0;
}
.src-empty {
    font-size: 0.85rem;
    color: #94a3b8;
    font-style: italic;
}

/* -- Strip Gradio default chrome around our cards ---- */
#question-box,
#answer-box,
#question-box label,
#question-box .container,
#question-box .form,
#question-box .wrap,
#answer-box .container,
#answer-box .form,
#answer-box .wrap {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
#answer-box {
    background: #fbfcfe !important;
    border: 1px solid var(--border) !important;
}
#question-box textarea {
    background: #f8fafc !important;
    color: var(--ink) !important;
}
"""

FORCE_LIGHT = """
function () {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.replace(url.href);
    }
}
"""

with gr.Blocks(css=CSS, js=FORCE_LIGHT, title="Cornell Tech Studio Guide") as demo:

    with gr.Column(elem_id="studio-app"):

        gr.HTML("""
        <div id="studio-header">
            <div class="logo">&#128172;</div>
            <h1>Cornell Tech Studio Guide</h1>
        </div>
        """)

        with gr.Row(equal_height=True):

            # -- Input panel (left) --------------------------------------------
            with gr.Column(elem_classes=["s-panel"]):
                question_box = gr.Textbox(
                    label="Your question",
                    placeholder='e.g. "What are the team size requirements for Startup Studio?"',
                    lines=4,
                    elem_id="question-box",
                )

                with gr.Column(elem_id="chips-row"):
                    gr.HTML('<span class="chips-label">Try asking</span>')
                    chip1 = gr.Button("Startup Studio team size?", elem_classes=["chip"])
                    chip2 = gr.Button("BigCo 2026 partners?", elem_classes=["chip"])
                    chip3 = gr.Button("2026 Award winners?", elem_classes=["chip"])
                    chip4 = gr.Button("Studio for founders?", elem_classes=["chip"])
                    chip5 = gr.Button("Student criticisms?", elem_classes=["chip"])

                ask_btn = gr.Button("Ask  \u2192", elem_id="ask-btn")

            # -- Answer panel (right) ------------------------------------------
            with gr.Column(elem_classes=["s-panel"]):
                gr.HTML("""
                <div class="answer-head">
                    <div class="avatar">CT</div>
                    <div>
                        <span class="answer-name">Studio Guide</span>
                        <span class="answer-sub">AI assistant</span>
                    </div>
                </div>
                """)
                answer_box = gr.Markdown(value=GREETING, elem_id="answer-box")

                sources_out = gr.HTML(
                    value='<div class="src-box"><p class="src-label">Retrieved from</p><span class="src-empty">sources will appear here after you ask a question</span></div>'
                )

    # Map chip clicks to filling the question box (native Gradio events)
    chip1.click(lambda: "Startup Studio team size requirements?", outputs=question_box)
    chip2.click(lambda: "What BigCo companies are partnering with Cornell Tech in 2026?", outputs=question_box)
    chip3.click(lambda: "Who won the 2026 Cornell Tech Startup Awards?", outputs=question_box)
    chip4.click(lambda: "I want to start my own company. Which Studio should I choose?", outputs=question_box)
    chip5.click(lambda: "What do students say are the weaknesses of the Studio program?", outputs=question_box)

    ask_btn.click(handle_query, inputs=question_box, outputs=[answer_box, sources_out])
    question_box.submit(handle_query, inputs=question_box, outputs=[answer_box, sources_out])


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  Cornell Tech Studio Guide - starting up")
    print("=" * 55 + "\n")
    run_ingestion()
    demo.launch()