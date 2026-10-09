# PDF Insight Agent (UC_05)

A RAG-based assistant that analyzes 50 PDFs: category, 2-line insight, detailed summary,
PDF-grounded Q&A with page citations, follow-up questions and multi-document comparison.

**Stack:** Python, Streamlit, Groq (LLM), PyMuPDF, Sentence Transformers, ChromaDB, python-dotenv.

## Run

```bash
pip install -r requirements.txt
cp .env.example .env            # then put your GROQ_API_KEY in .env
python scripts/ingest.py        # builds the vector DB from dataset/*.pdf
streamlit run app.py
```

## How to use

- **One PDF selected** (sidebar): shows its category and 2-line insight; button for a detailed summary; questions are answered from that PDF.
- **Several PDFs selected**: questions retrieve from each PDF separately, for comparisons.
- **None selected**: questions search all 50 PDFs.
- Ask follow-ups ("why?", "explain the second point") — the last few turns are remembered.
- If nothing relevant is found, the agent replies: *"I couldn't find sufficient information about this in the provided documents."*

## File map

| File | Role |
|---|---|
| `app.py` | Streamlit UI |
| `agent.py` | Orchestrates insight, summary and Q&A |
| `llm.py` | Groq API call |
| `pdf_processor.py` | PDF text extraction per page |
| `chunker.py` | Overlapping word chunks, keeps page numbers |
| `embeddings.py` | Sentence Transformers embeddings |
| `vector_store.py` | ChromaDB add / search / read |
| `retriever.py` | Picks relevant chunks (single, multi, or all docs) |
| `memory.py` | Follow-up conversation memory |
| `citations.py` | Context blocks and `Sources` list |
| `prompts.py` | All prompts |
| `config.py` | Paths, model names, settings |
| `scripts/ingest.py` | Builds the vector DB |

## Notes

- `PDF_43_Atmospheric_aerosol.pdf` contains only a title and a placeholder line, so the agent reports it has too little text instead of inventing an insight.
- Tune `MAX_DISTANCE` in `config.py` if answers are refused too often (raise it) or off-topic chunks get through (lower it).
