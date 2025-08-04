import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.dossier.living_dossier import LivingDossier
from backend.dossier.models import LinguisticProfileEntry, PsychProfileEntry


def test_store_dossier_updates_indexes() -> None:
    dossier = {
        "inner_world": {
            "backstory": "A humble origin",
            "memory_journal": [
                {
                    "event": "Saved a cat",
                    "emotion": "pride",
                    "sensory_anchor": "soft fur",
                    "influence_on_present": "compassion",
                }
            ],
            "core_motivation": "Seek justice",
            "primal_fear": "failure",
            "primary_defense_mechanism": "humor",
            "central_paradox": "brave yet fearful",
            "magic_if": "What if?",
        },
        "blueprint": {
            "linguistic_profile": {
                "vocabulary_syntax": "formal",
                "rhythm_imagery": "poetic",
            }
        },
    }

    dossier_store = LivingDossier()
    dossier_store.store_dossier(dossier)

    psych_items = dossier_store.psych_profile_index._items
    psych_ids = {e.id for e in psych_items}
    assert "core_motivation" in psych_ids
    assert "memory_journal_0" in psych_ids
    assert len(psych_ids) == 7
    assert all(isinstance(e, PsychProfileEntry) for e in psych_items)

    ling_items = dossier_store.linguistic_profile_index._items
    ling_ids = {e.id for e in ling_items}
    assert ling_ids == {"vocabulary_syntax", "rhythm_imagery"}
    assert all(isinstance(e, LinguisticProfileEntry) for e in ling_items)
