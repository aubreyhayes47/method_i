"""Demonstrate the CharacterExtractionPipeline on Project Gutenberg texts.

The script downloads "Pride and Prejudice" by default (Gutenberg book ID
1342) and prints the most common character names detected in the text. The
pipeline stages here use simple heuristics so the demo runs without external
LLM dependencies.

To analyze a different book, change ``book_id`` below to another Project
Gutenberg identifier. For other data sources, adjust the ``fetch_text`` method.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List

from backend.casting.pipeline import CharacterExtractionPipeline
from backend.casting.sources import gutenberg


class RegexLLMClient:
    """Very small stand-in for an LLM that finds capitalized name phrases."""

    name_pattern = re.compile(
        r"(?:Mr|Mrs|Miss|Ms|Dr)\.\s+[A-Z][a-z]+|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
    )
    blacklist = {
        "Project Gutenberg",
        "The Project Gutenberg",
        "Pride And Prejudice",
        "Gutenberg",
        "Chapter",
        "Volume",
    }

    def generate(self, prompt: str):
        text = prompt.split("Text:\n", 1)[-1]
        names = [n.strip() for n in self.name_pattern.findall(text)]
        names = [n for n in names if n not in self.blacklist]
        return {"characters": [{"name": n} for n in names]}


class SimpleCharacterExtractionPipeline(CharacterExtractionPipeline):
    """Minimal pipeline with Gutenberg download and naive chunking."""

    def fetch_text(self, book_id: str, source: str) -> str:  # pragma: no cover
        if source != "gutenberg":
            raise ValueError(f"Unsupported source: {source}")
        # Swap this out to integrate other sources such as local files or APIs.
        return gutenberg.fetch_text(int(book_id))

    def chunk_text(self, text: str) -> List[str]:  # pragma: no cover
        words = text.split()
        chunk_size = 1000
        chunks: List[str] = []
        for i in range(0, len(words), chunk_size):
            chunks.append(" ".join(words[i : i + chunk_size]))
        return chunks


def main() -> None:
    book_id = 1342  # Pride and Prejudice; adjust to another ID as desired.
    pipeline = SimpleCharacterExtractionPipeline(llm_client=RegexLLMClient())
    candidates = pipeline.run(str(book_id))

    counts = Counter({c.name: len(c.source_chunks) for c in candidates})
    for name, freq in counts.most_common(10):
        print(f"{name}: {freq}")


if __name__ == "__main__":
    main()
