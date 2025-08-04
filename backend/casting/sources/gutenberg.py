"""Utilities for fetching texts from Project Gutenberg."""
from __future__ import annotations

import gzip
import io
import re
import zipfile

import requests

GUTENBERG_BASE_URL = "https://www.gutenberg.org/files"


def _find_candidate(haystack: str, pattern: str) -> str | None:
    """Return the first file name matching ``pattern`` in ``haystack``."""
    match = re.search(pattern, haystack, re.IGNORECASE)
    return match.group(1) if match else None


def download_text(book_id: int) -> str:
    """Download raw text for ``book_id`` from Project Gutenberg.

    The directory listing for the book is parsed via regex to locate a
    plain-text file.  If no direct text file is available a compressed
    variant (``.txt.gz`` or ``.zip``) is downloaded and extracted.
    """
    base = f"{GUTENBERG_BASE_URL}/{book_id}"
    listing = requests.get(base)
    listing.raise_for_status()

    text_name = _find_candidate(listing.text, r'href="([^\"]+\.txt(?:\.utf-8)?)"')
    if text_name:
        resp = requests.get(f"{base}/{text_name}")
        resp.raise_for_status()
        return resp.text

    gz_name = _find_candidate(listing.text, r'href="([^\"]+\.txt\.gz)"')
    if gz_name:
        resp = requests.get(f"{base}/{gz_name}")
        resp.raise_for_status()
        return gzip.decompress(resp.content).decode("utf-8")

    zip_name = _find_candidate(listing.text, r'href="([^\"]+\.zip)"')
    if zip_name:
        resp = requests.get(f"{base}/{zip_name}")
        resp.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(resp.content)) as archive:
            first = archive.namelist()[0]
            data = archive.read(first)
        return data.decode("utf-8")

    raise ValueError(f"Could not locate text for book id {book_id}")


def fetch_text(book_id: int) -> str:
    """Public interface used by the pipeline's ``fetch_text`` stage."""
    return download_text(book_id)
