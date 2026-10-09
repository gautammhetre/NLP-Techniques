"""Streamlit UI for PDF Insight Agent.  Run:  streamlit run app.py"""
import streamlit as st

from agent import PDFInsightAgent
from config import GROQ_API_KEY

st.set_page_config(page_title="PDF Insight Agent", page_icon="📄", layout="wide")
st.title("📄 PDF Insight Agent")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Create a file named `.env` (not `.env.example`) in this folder containing "
             "`GROQ_API_KEY=your_key`, then restart the app.")
    st.stop()

# Keep one agent (and its memory) per browser session
if "agent" not in st.session_state:
    st.session_state.agent = PDFInsightAgent()
    st.session_state.messages = []
    st.session_state.cache = {}   # (kind, doc) -> generated text
agent = st.session_state.agent

docs = agent.documents()
if not docs:
    st.warning("The vector database is empty. Run `python scripts/ingest.py` first.")
    st.stop()


def cached(kind, doc, func):
    key = (kind, doc)
    if key not in st.session_state.cache:
        with st.spinner(f"Generating {kind}..."):
            st.session_state.cache[key] = func(doc)
    return st.session_state.cache[key]


# ---- Sidebar: PDF selection ----
with st.sidebar:
    st.header("Select PDF(s)")
    selected = st.multiselect(
        "Choose one PDF to analyze, or several to compare. Leave empty to search all PDFs.", docs
    )
    if st.button("Clear conversation"):
        agent.memory.clear()
        st.session_state.messages = []
        st.rerun()

# ---- Single document view: category, insight, summary ----
if len(selected) == 1:
    doc = selected[0]
    st.subheader(doc)
    st.markdown(cached("overview", doc, agent.overview))
    if st.button("Show detailed summary"):
        st.session_state.show_summary = doc
    if st.session_state.get("show_summary") == doc:
        with st.expander("Detailed summary", expanded=True):
            st.markdown(cached("summary", doc, agent.summary))
elif len(selected) > 1:
    st.info("Comparing: " + ", ".join(f"`{d}`" for d in selected))
else:
    st.info("Searching across all PDFs. Select a PDF in the sidebar to see its category, insight and summary.")

st.divider()

# ---- Chat ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question about the PDFs...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the PDFs..."):
            try:
                answer, chunks = agent.answer(question, selected)
                sources = agent.sources_text(chunks)
                reply = answer + ("\n\n" + sources if sources else "")
            except Exception as e:
                reply = f"Something went wrong: {e}"
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
