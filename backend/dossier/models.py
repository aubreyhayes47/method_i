from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


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


@dataclass
class Character:
    """Represents a stored character dossier."""

    character_id: str
    dossier: Dict[str, Any]


class CharacterStore:
    """Simple in-memory persistence for ``Character`` instances."""

    def __init__(self) -> None:
        self._characters: Dict[str, Character] = {}

    def insert(self, dossier: Dict[str, Any], character_id: Optional[str] = None) -> str:
        """Persist ``dossier`` under a unique ``character_id``.

        If ``character_id`` is not supplied, a random UUID4 string is used.
        """

        cid = character_id or str(uuid4())
        if cid in self._characters:
            raise ValueError(f"character_id '{cid}' already exists")
        self._characters[cid] = Character(character_id=cid, dossier=dossier)
        return cid

    def get(self, character_id: str) -> Optional[Character]:
        """Retrieve a stored ``Character`` by its id."""

        return self._characters.get(character_id)

    def all(self) -> List[Character]:
        """Return all persisted characters."""

        return list(self._characters.values())
