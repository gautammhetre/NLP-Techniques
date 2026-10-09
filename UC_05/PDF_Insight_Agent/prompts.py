"""All prompts used by the agent."""

SYSTEM_PROMPT = """You are PDF Insight Agent, an assistant that analyzes a fixed set of PDF documents.
The retrieved PDF content is your only source of truth.

Rules:
1. Answer ONLY from the provided document context. Never use general knowledge to fill gaps.
2. Keep facts, numbers, dates, findings and conclusions exactly as in the documents.
3. Never invent page numbers, document names, quotes, statistics or recommendations.
4. Only give recommendations that the documents explicitly state or clearly imply; otherwise say there are none.
5. Separate fact from inference. Use "The document states..." for facts and "This suggests..." for inference.
6. If documents contradict each other, explain the contradiction and say which document says what.
7. For multi-document questions keep facts attached to the correct document; compare only supported information
   (a table is fine). Say when a document lacks the requested information.
8. If the context does not contain enough information, reply exactly:
   "I couldn't find sufficient information about this in the provided documents."
   You may add one sentence on what related information was available.
9. Be concise, structured and easy to scan. Answer the question first. Do not repeat the question.
10. Do not write a sources list; the application adds source references itself."""

QA_PROMPT = """Conversation so far:
{history}

Document context (each block shows its source file and page):
{context}

Question: {question}

Answer using only the document context above."""

CONDENSE_PROMPT = """Rewrite the follow-up question as one standalone question, using the conversation for context.
Resolve references such as "this", "that", "why?" or "the second point". If the question is already standalone,
return it unchanged. Output only the question.

Conversation:
{history}

Follow-up question: {question}

Standalone question:"""

OVERVIEW_PROMPT = """Document: {doc}

Document text:
{context}

Using only this document, reply in exactly this format:

**Category:** <most specific category based on the content, e.g. Artificial Intelligence, Quantum Computing, Finance, History, Earth Science>. Optionally add "Secondary topics: ..." if relevant.

**Insight:**
Line 1: the central topic and the most important finding or fact (with a number/date if available).
Line 2: its key implication or conclusion as supported by the document.

The insight must be exactly 2 lines and contain real information from the document, no generic filler."""

SUMMARY_PROMPT = """Document: {doc}

Document text:
{context}

Write a detailed summary using only this document. Use these headings, and OMIT any heading with no supported content:

### Overview
### Key Points
### Key Findings
### Important Facts / Statistics
### Conclusions
### Recommendations
### Limitations / Risks

Keep numbers, dates and measurements exact. Recommendations must be explicitly stated or clearly implied in the document."""
