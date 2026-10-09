"""Main agent: ties retrieval, prompts, the LLM, memory and citations together."""
from citations import build_context, format_sources
from config import MIN_DOC_CHARS
from llm import ask_llm
from memory import ConversationMemory
from prompts import CONDENSE_PROMPT, OVERVIEW_PROMPT, QA_PROMPT, SUMMARY_PROMPT
from retriever import get_document_text, retrieve
from vector_store import list_documents

NOT_FOUND = "I couldn't find sufficient information about this in the provided documents."
TOO_SHORT = ("This document contains too little text to analyze "
             "(it only has a title and placeholder line), so I can't give a reliable insight or summary.")


class PDFInsightAgent:
    def __init__(self):
        self.memory = ConversationMemory()

    def documents(self):
        return list_documents()

    def _doc_text(self, doc):
        text = get_document_text(doc)
        return text if len(text) >= MIN_DOC_CHARS else None

    # --- per-document features -------------------------------------------------
    def overview(self, doc):
        """Category + 2-line insight."""
        text = self._doc_text(doc)
        if text is None:
            return TOO_SHORT
        return ask_llm(OVERVIEW_PROMPT.format(doc=doc, context=text))

    def summary(self, doc):
        """Detailed structured summary."""
        text = self._doc_text(doc)
        if text is None:
            return TOO_SHORT
        return ask_llm(SUMMARY_PROMPT.format(doc=doc, context=text))

    # --- question answering ----------------------------------------------------
    def answer(self, question, selected_docs=None):
        """RAG answer. Returns (answer_text, source_chunks)."""
        # 1. Turn follow-ups ("why?") into standalone questions for better retrieval
        search_query = question
        if not self.memory.is_empty():
            search_query = ask_llm(
                CONDENSE_PROMPT.format(history=self.memory.as_text(), question=question), temperature=0
            )

        # 2. Retrieve evidence from the PDFs
        chunks = retrieve(search_query, selected_docs)
        if not chunks:
            self.memory.add(question, NOT_FOUND)
            return NOT_FOUND, []

        # 3. Ask the LLM to answer only from that evidence
        prompt = QA_PROMPT.format(
            history=self.memory.as_text(), context=build_context(chunks), question=question
        )
        answer = ask_llm(prompt)
        self.memory.add(question, answer)

        # 4. Don't show sources when the model says nothing was found
        if "couldn't find sufficient information" in answer:
            return answer, []
        return answer, chunks

    def sources_text(self, chunks):
        return format_sources(chunks)
