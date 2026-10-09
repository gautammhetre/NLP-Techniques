"""Build context blocks and source/page references from retrieved chunks."""


def build_context(chunks):
    """Text block sent to the LLM; each chunk is labelled with its file and page."""
    return "\n\n".join(f"[Source: {c['doc']}, Page {c['page']}]\n{c['text']}" for c in chunks)


def format_sources(chunks):
    """Markdown list of unique (document, page) references."""
    pairs = sorted({(c["doc"], c["page"]) for c in chunks})
    if not pairs:
        return ""
    lines = [f"- `{doc}`, Page {page}" for doc, page in pairs]
    return "**Sources:**\n" + "\n".join(lines)
