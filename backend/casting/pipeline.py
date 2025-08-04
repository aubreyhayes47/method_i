from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import re
from difflib import SequenceMatcher

from .models import CharacterCandidate, CastingCallLogStore
from .prompts import CASTING_DIRECTOR_PROMPT
from ..llm import LLMClient


@dataclass
class CharacterExtractionPipeline:
    """Pipeline orchestrating character extraction from source texts."""

    llm_client: LLMClient
    store: Optional[CastingCallLogStore] = None

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
        deduped = self.deduplicate_candidates(candidates)
        flagged = self.flag_duplicate_candidates(deduped)

        if self.store is not None:
            for cand in flagged:
                self.store.add(cand)

        return flagged

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
        for idx, chunk in enumerate(chunks):
            prompt = f"{CASTING_DIRECTOR_PROMPT}\n{chunk}"
            response = self.llm_client.generate(prompt)
            for item in response.get("characters", []):
                try:
                    candidate = CharacterCandidate(**item)
                    candidate.source_chunks.append(idx)
                    candidates.append(candidate)
                except TypeError:
                    continue
        return candidates

    def deduplicate_candidates(
        self, candidates: List[CharacterCandidate]
    ) -> List[CharacterCandidate]:
        """Deduplicate similar character candidates.

        Parameters
        ----------
        candidates:
            List of raw ``CharacterCandidate`` instances extracted from text
            chunks. Each candidate should carry provenance information in its
            ``source_chunks`` attribute.

        Returns
        -------
        list[CharacterCandidate]
            Consolidated list of candidates with merged ``source_chunks``.
        """

        def normalize(name: str) -> str:
            """Lower-case and strip non-alphanumeric characters."""
            return re.sub(r"[^a-z0-9]", "", name.lower())

        merged: dict[str, CharacterCandidate] = {}
        for cand in candidates:
            norm = normalize(cand.name)

            # Attempt fuzzy match against existing normalized keys.
            match_key = None
            for key in merged.keys():
                ratio = SequenceMatcher(None, norm, key).ratio()
                if ratio >= 0.85:
                    match_key = key
                    break

            if match_key is None:
                merged[norm] = CharacterCandidate(
                    name=cand.name, source_chunks=list(cand.source_chunks)
                )
            else:
                existing = merged[match_key]
                existing.source_chunks.extend(cand.source_chunks)
                # ensure unique provenance entries
                existing.source_chunks = sorted(set(existing.source_chunks))

        return list(merged.values())

    def flag_duplicate_candidates(
        self, candidates: List[CharacterCandidate]
    ) -> List[CharacterCandidate]:
        """Mark candidates that are duplicates or likely minor roles.

        Candidates sharing identical ``source_chunks`` sets are flagged as
        duplicates. Candidates that appear in only a single chunk are flagged as
        minor roles.
        """

        groups: dict[tuple[int, ...], List[CharacterCandidate]] = {}
        for cand in candidates:
            key = tuple(sorted(cand.source_chunks))
            groups.setdefault(key, []).append(cand)

        for group in groups.values():
            if len(group) > 1:
                for cand in group:
                    cand.duplicate = True

        for cand in candidates:
            if len(cand.source_chunks) <= 1:
                cand.minor_role = True

        return candidates
