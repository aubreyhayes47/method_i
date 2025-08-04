from dataclasses import dataclass, field
from typing import Any, Dict, List

from .indexes import ListIndex
from .models import LinguisticProfileEntry, PsychProfileEntry


@dataclass
class LivingDossier:
    """Container for various dossier indices."""

    psych_profile_index: ListIndex = field(default_factory=ListIndex)
    linguistic_profile_index: ListIndex = field(default_factory=ListIndex)

    def add_psych_profile(self, item: Any) -> None:
        self.psych_profile_index.add(item)

    def add_linguistic_profile(self, item: Any) -> None:
        self.linguistic_profile_index.add(item)

    def parse_psych_profile(self, dossier: Dict[str, Any]) -> List[PsychProfileEntry]:
        """Extract ``PsychProfileEntry`` objects from ``dossier``.

        The method looks for an ``inner_world`` section and converts its
        textual fields and memory journal entries into ``PsychProfileEntry``
        instances.
        """

        entries: List[PsychProfileEntry] = []
        inner_world = dossier.get("inner_world", {})

        for key, value in inner_world.items():
            if key == "memory_journal" and isinstance(value, list):
                for idx, item in enumerate(value):
                    parts = [
                        f"{sub_key.replace('_', ' ').title()}: {sub_val}"
                        for sub_key, sub_val in item.items()
                    ]
                    content = "; ".join(parts)
                    entries.append(
                        PsychProfileEntry(
                            id=f"memory_journal_{idx}", content=content
                        )
                    )
            elif isinstance(value, str):
                entries.append(PsychProfileEntry(id=key, content=value))

        return entries

    def parse_linguistic_profile(
        self, dossier: Dict[str, Any]
    ) -> List[LinguisticProfileEntry]:
        """Extract ``LinguisticProfileEntry`` objects from ``dossier``.

        Data is pulled from ``blueprint.linguistic_profile`` and each string
        field becomes an entry.
        """

        entries: List[LinguisticProfileEntry] = []
        blueprint = dossier.get("blueprint", {})
        profile = blueprint.get("linguistic_profile", {})

        for key, value in profile.items():
            if isinstance(value, str):
                entries.append(LinguisticProfileEntry(id=key, content=value))

        return entries

    def store_dossier(self, dossier: Dict[str, Any]) -> None:
        """Store ``dossier`` and update profile indexes."""

        for entry in self.parse_psych_profile(dossier):
            self.add_psych_profile(entry)
        for entry in self.parse_linguistic_profile(dossier):
            self.add_linguistic_profile(entry)
