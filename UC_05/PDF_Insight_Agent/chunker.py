"""Split page text into overlapping word-based chunks, keeping the page number."""
from config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_pages(pages):
    """Turn page dicts into chunk dicts: {"doc", "page", "text", "chunk_id"}."""
    chunks = []
    step = CHUNK_SIZE - CHUNK_OVERLAP
    for page in pages:
        words = page["text"].split()
        for start in range(0, len(words), step):
            piece = " ".join(words[start:start + CHUNK_SIZE])
            # skip a tiny tail that is already covered by the previous chunk's overlap
            if start > 0 and len(piece.split()) <= CHUNK_OVERLAP:
                break
            chunks.append({
                "doc": page["doc"],
                "page": page["page"],
                "text": piece,
                "chunk_id": f"{page['doc']}_p{page['page']}_{start}",
            })
    return chunks
