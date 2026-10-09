"""Extract text from PDFs page by page using PyMuPDF."""
from pathlib import Path

import pymupdf


def extract_pages(pdf_path):
    """Return a list of {"doc", "page", "text"} dicts (page numbers start at 1)."""
    pages = []
    with pymupdf.open(pdf_path) as pdf:
        for number, page in enumerate(pdf, start=1):
            text = page.get_text().strip()
            if text:
                pages.append({"doc": Path(pdf_path).name, "page": number, "text": text})
    return pages
