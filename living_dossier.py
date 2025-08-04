from __future__ import annotations
from typing import Dict, List, Any


class LivingDossier:
    """Simple in-memory character dossier.

    This class simulates retrieval of memories and linguistic traits for
    characters by ID.  A real implementation would likely query a database or
    vector store.  For the purposes of the pipeline demonstration we keep the
    data in dictionaries provided at initialisation time.
    """

    def __init__(self, memories: Dict[str, List[str]] | None = None,
                 linguistic_traits: Dict[str, Dict[str, Any]] | None = None) -> None:
        self._memories = memories or {}
        self._linguistic_traits = linguistic_traits or {}

    def retrieve_memories(self, character_id: str) -> List[str]:
        """Return the memories for *character_id*.

        Parameters
        ----------
        character_id: str
            Unique identifier for the character.
        """
        return self._memories.get(character_id, [])

    def retrieve_linguistic_traits(self, character_id: str) -> Dict[str, Any]:
        """Return the linguistic traits for *character_id*.

        Parameters
        ----------
        character_id: str
            Unique identifier for the character.
        """
        return self._linguistic_traits.get(character_id, {})
