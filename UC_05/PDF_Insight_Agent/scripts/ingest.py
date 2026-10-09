"""Read every PDF in dataset/, chunk it, embed it and store it in ChromaDB.

Run from the project folder:  python scripts/ingest.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chunker import chunk_pages
from config import DATASET_DIR
from embeddings import embed_texts
from pdf_processor import extract_pages
from vector_store import add_chunks, reset_collection


def main():
    pdf_files = sorted(DATASET_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {DATASET_DIR}. Put your PDFs there and run again.")
        return

    reset_collection()
    total_chunks = 0
    for pdf in pdf_files:
        pages = extract_pages(pdf)
        chunks = chunk_pages(pages)
        if not chunks:
            print(f"  skipped (no text): {pdf.name}")
            continue
        add_chunks(chunks, embed_texts([c["text"] for c in chunks]))
        total_chunks += len(chunks)
        print(f"  {pdf.name}: {len(pages)} pages, {len(chunks)} chunks")

    print(f"\nDone. {len(pdf_files)} PDFs, {total_chunks} chunks stored.")


if __name__ == "__main__":
    main()
