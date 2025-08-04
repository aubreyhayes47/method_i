from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class _BaseEntry:
    """Common fields for dossier entries."""
    id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    embedding: Optional[List[float]] = field(default=None)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("id is required")
        if not self.content:
            raise ValueError("content is required")


@dataclass
class PsychProfileEntry(_BaseEntry):
    """Represents an entry in the psychological profile."""


@dataclass
class LinguisticProfileEntry(_BaseEntry):
    """Represents an entry in the linguistic profile."""


@dataclass
class LivingDossier(_BaseEntry):
    """High level dossier entry aggregating profile information."""
