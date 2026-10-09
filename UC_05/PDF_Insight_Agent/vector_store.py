"""ChromaDB operations: store chunks, search them, read a document back."""
import chromadb

from config import COLLECTION_NAME, VECTOR_DB_DIR


def _collection():
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    return client.get_or_create_collection(COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def reset_collection():
    """Delete the old collection so ingestion starts clean."""
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass


def add_chunks(chunks, vectors):
    _collection().add(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=vectors,
        metadatas=[{"doc": c["doc"], "page": c["page"]} for c in chunks],
    )


def search(query_vector, n_results, doc=None):
    """Return chunks sorted by similarity. Optionally restrict to one document."""
    where = {"doc": doc} if doc else None
    result = _collection().query(query_embeddings=[query_vector], n_results=n_results, where=where)
    return [
        {"doc": m["doc"], "page": m["page"], "text": t, "distance": d}
        for t, m, d in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])
    ]


def get_document_chunks(doc):
    """All chunks of one document in reading order (page, then position)."""
    result = _collection().get(where={"doc": doc})
    chunks = [
        {"doc": m["doc"], "page": m["page"], "text": t, "id": i}
        for t, m, i in zip(result["documents"], result["metadatas"], result["ids"])
    ]
    # chunk ids end with the word offset, so sort by page then offset
    chunks.sort(key=lambda c: (c["page"], int(c["id"].rsplit("_", 1)[1])))
    return chunks


def list_documents():
    result = _collection().get(include=["metadatas"])
    return sorted({m["doc"] for m in result["metadatas"]})
