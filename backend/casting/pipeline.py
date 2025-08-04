from __future__ import annotations
from dataclasses import dataclass
from typing import List

from .models import CharacterCandidate
from .prompts import CASTING_DIRECTOR_PROMPT
from ..llm import LLMClient


@dataclass
class CharacterExtractionPipeline:
    """Pipeline orchestrating character extraction from source texts."""

    llm_client: LLMClient

    def run(
        self, book_id: str, source: str = "gutenberg"
    ) -> List[CharacterCandidate]:
        """Run the character extraction pipeline for a given book.

        Parameters
        ----------
        book_id:
            Identifier of the book to process.
        source:
            Source from which the book text will be fetched. Defaults to
            ``"gutenberg"``.

        Returns
        -------
        list[CharacterCandidate]
            Deduplicated list of character candidates extracted from the text.
        """
        text = self.fetch_text(book_id, source)
        chunks = self.chunk_text(text)
        candidates = self.extract_characters(chunks)
        return self.deduplicate_candidates(candidates)

    # The following methods are expected to be implemented by subclasses or
    # provided via mixins. They are declared here to document the expected
    # interface of the pipeline steps.
    def fetch_text(
        self, book_id: str, source: str
    ) -> str:  # pragma: no cover
        """Retrieve the raw text for ``book_id`` from ``source``."""
        raise NotImplementedError

    def chunk_text(self, text: str) -> List[str]:  # pragma: no cover
        """Split raw text into smaller chunks for analysis."""
        raise NotImplementedError

    def extract_characters(
        self, chunks: List[str]
    ) -> List[CharacterCandidate]:
        """Extract character candidates from text chunks."""

        candidates: List[CharacterCandidate] = []
        for chunk in chunks:
            prompt = f"{CASTING_DIRECTOR_PROMPT}\n{chunk}"
            response = self.llm_client.generate(prompt)
            for item in response.get("characters", []):
                try:
                    candidates.append(CharacterCandidate(**item))
                except TypeError:
                    continue
        return candidates

    def deduplicate_candidates(
        self, candidates: List[CharacterCandidate]
    ) -> List[CharacterCandidate]:  # pragma: no cover
        """Deduplicate similar character candidates."""
        raise NotImplementedError
