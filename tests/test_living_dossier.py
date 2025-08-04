import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from living_dossier import LivingDossier


def test_retrieve_memories_by_character_id():
    dossier = LivingDossier(
        memories={"char1": ["Loves pizza"], "char2": ["Enjoys pasta"]}
    )
    assert dossier.retrieve_memories("char1") == ["Loves pizza"]
    assert dossier.retrieve_memories("unknown") == []


def test_retrieve_linguistic_traits_by_character_id():
    traits = {"char1": {"style": "formal"}}
    dossier = LivingDossier(linguistic_traits=traits)
    assert dossier.retrieve_linguistic_traits("char1") == {"style": "formal"}
    assert dossier.retrieve_linguistic_traits("missing") == {}
