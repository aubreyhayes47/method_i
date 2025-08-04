"""Data models for the casting pipeline."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CharacterCandidate:
    """Represents an extracted character candidate.

    Attributes
    ----------
    name:
        Candidate name extracted from a chunk of text.
    source_chunks:
        List of chunk indices where the candidate was mentioned. This enables
        provenance tracking when candidates are deduplicated.
    """

    name: str
    source_chunks: List[int] = field(default_factory=list)
    duplicate: bool = False
    minor_role: bool = False


@dataclass
class CastingCallLog:
    """Record of a candidate considered during a casting call."""

    candidate: CharacterCandidate
    selected: bool = False


class CastingCallLogStore:
    """Simple in-memory persistence for ``CastingCallLog`` entries."""

    def __init__(self) -> None:
        self._logs: List[CastingCallLog] = []

    def add(self, candidate: CharacterCandidate, selected: bool = False) -> None:
        """Persist a candidate to the log."""

        self._logs.append(CastingCallLog(candidate=candidate, selected=selected))

    def all(self) -> List[CastingCallLog]:
        """Return all log entries."""

        return list(self._logs)
