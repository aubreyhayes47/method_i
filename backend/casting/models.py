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
