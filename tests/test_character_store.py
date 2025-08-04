import pytest

from backend.dossier.models import CharacterStore


def test_insert_and_retrieve_character():
    store = CharacterStore()
    dossier = {"name": "Alice"}
    cid = store.insert(dossier)
    stored = store.get(cid)
    assert stored is not None
    assert stored.dossier == dossier


def test_insert_duplicate_id_raises():
    store = CharacterStore()
    dossier = {"name": "Bob"}
    cid = store.insert(dossier, character_id="abc")
    assert cid == "abc"
    with pytest.raises(ValueError):
        store.insert({"name": "Charlie"}, character_id="abc")
