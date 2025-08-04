from dataclasses import dataclass, field
from typing import Any

from .indexes import ListIndex


@dataclass
class LivingDossier:
    """Container for various dossier indices."""

    psych_profile_index: ListIndex = field(default_factory=ListIndex)
    linguistic_profile_index: ListIndex = field(default_factory=ListIndex)

    def add_psych_profile(self, item: Any) -> None:
        self.psych_profile_index.add(item)

    def add_linguistic_profile(self, item: Any) -> None:
        self.linguistic_profile_index.add(item)
