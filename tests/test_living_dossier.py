import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from living_dossier import LivingDossier


def test_retrieve_memories_ranks_by_occurrence():
    dossier = LivingDossier(
        memories=[
            "Loves pizza",
            "Pizza is delicious and pizza is life",
            "Enjoys pasta",
        ]
    )
    results = dossier.retrieve_memories("pizza")
    assert results[0][1] == "Pizza is delicious and pizza is life"
    assert results[0][0] > results[1][0]


def test_retrieve_linguistic_traits():
    dossier = LivingDossier(linguistic_traits=["uses slang", "formal tone"])
    assert dossier.retrieve_linguistic_traits("slang") == [(1, "uses slang")]
