"""Find the PDF chunks that are relevant to a question."""
from config import MAX_DISTANCE, MAX_DOC_CONTEXT_CHARS, TOP_K, TOP_K_PER_DOC
from embeddings import embed_query
from vector_store import get_document_chunks, search


def retrieve(question, selected_docs=None):
    """
    - no document selected   -> search all PDFs
    - one document selected  -> search only that PDF
    - several selected       -> search each PDF separately (multi-document question)
    Chunks that are too dissimilar are dropped, so an empty list means "not found".
    """
    vector = embed_query(question)
    selected_docs = selected_docs or []

    if not selected_docs:
        found = search(vector, TOP_K)
    elif len(selected_docs) == 1:
        found = search(vector, TOP_K, doc=selected_docs[0])
    else:
        found = []
        for doc in selected_docs:
            found += search(vector, TOP_K_PER_DOC, doc=doc)

    return [c for c in found if c["distance"] <= MAX_DISTANCE]


def get_document_text(doc):
    """Representative text of one document for insight / summary (evenly sampled if long)."""
    chunks = get_document_chunks(doc)
    total = sum(len(c["text"]) for c in chunks)
    if total > MAX_DOC_CONTEXT_CHARS:
        # keep evenly spaced chunks so the whole document is covered
        avg = total / len(chunks)
        keep = max(1, int(MAX_DOC_CONTEXT_CHARS / avg))
        chunks = [chunks[int(i * len(chunks) / keep)] for i in range(keep)]
    return "\n\n".join(f"[Page {c['page']}] {c['text']}" for c in chunks)
