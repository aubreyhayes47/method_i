import os
import sys
from typing import List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Ensure repository root on path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.casting.api import casting_call_log, router
from backend.casting.models import CharacterCandidate
from backend.casting.pipeline import DossierCompiler
from backend.dossier.living_dossier import LivingDossier


class DummyLLMClient:
    """LLM client returning predetermined results."""

    def __init__(self, results: List[dict]) -> None:
        self._results = results
        self._idx = 0

    def generate(self, prompt: str) -> dict:
        result = self._results[self._idx]
        if self._idx < len(self._results) - 1:
            self._idx += 1
        return result


class DummyStore:
    """Store that records inserts and populates indexes."""

    def __init__(self) -> None:
        self.inserted: List[dict] = []
        self.living_dossier = LivingDossier()

    def insert(self, dossier: dict) -> None:
        self.inserted.append(dossier)
        self.living_dossier.store_dossier(dossier)


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture
def store(monkeypatch: pytest.MonkeyPatch) -> DummyStore:
    store = DummyStore()
    monkeypatch.setattr("backend.casting.api.character_store", store)
    return store


@pytest.fixture(autouse=True)
def clear_state() -> None:
    casting_call_log._logs.clear()


def add_candidates() -> None:
    casting_call_log.add(CharacterCandidate(name="Jane"))
    casting_call_log.add(CharacterCandidate(name="Tom"))


def test_compile_stores_dossier_and_indexes(
    client: TestClient, store: DummyStore, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Valid dossiers are stored and indexed; invalid ones yield errors."""

    add_candidates()
    client.post("/casting-call/select", json={"selected_ids": [0, 1]})

    valid_dossier = {
        "name": "Jane",
        "role": "protagonist",
        "source_material": "demo",
        "blueprint": {
            "verifiable_facts": ["fact"],
            "linguistic_profile": {
                "vocabulary_syntax": "formal",
                "rhythm_imagery": "poetic",
            },
            "objective_action_analysis": {"super_objective": "goal"},
            "relationship_mapping": [
                {"character": "Tom", "emotional_currency": "trust"}
            ],
        },
        "inner_world": {
            "backstory": "origin",
            "memory_journal": [
                {
                    "event": "saved",
                    "emotion": "pride",
                    "sensory_anchor": "fur",
                    "influence_on_present": "compassion",
                }
            ],
            "core_motivation": "justice",
            "primal_fear": "failure",
            "primary_defense_mechanism": "humor",
            "central_paradox": "brave yet afraid",
            "magic_if": "what if",
        },
        "physical_form": {
            "animal_work": {
                "animal": "lion",
                "effort_rhythm": "strong",
                "translated_human_quality": "bravery",
            },
            "chekhov_technique": {
                "energetic_center": "solar plexus",
                "imaginary_body": {
                    "posture": "upright",
                    "weight_distribution": "balanced",
                    "tension_patterns": "loose",
                },
            },
        },
        "method_work": {
            "stanislavski": {
                "given_circumstances": "scene",
                "magic_if": "as if",
                "through_line_of_action": "win",
            },
            "uta_hagen": {
                "nine_questions": {
                    "who_am_i": "Jane",
                    "what_do_i_want": "peace",
                    "why_do_i_want_it": "safety",
                }
            },
            "chekhov": {
                "psychological_gesture": "reach",
                "imaginary_body": "light",
            },
            "practical_aesthetics": {
                "literal": "literal",
                "want": "want",
                "essential_action": "act",
                "as_if": "as if",
            },
        },
    }

    invalid_dossier = {"name": "Tom"}

    dummy_llm = DummyLLMClient([valid_dossier, invalid_dossier])
    monkeypatch.setattr(
        "backend.casting.api.compiler_factory",
        lambda: DossierCompiler(llm_client=dummy_llm),
    )

    response = client.post(
        "/casting-call/compile", json={"candidate_ids": [0, 1]}
    )
    assert response.status_code == 200
    data = response.json()

    assert data[0]["name"] == "Jane"
    assert "error" not in data[0]
    assert data[1]["name"] == "Tom"
    assert "error" in data[1]

    assert len(store.inserted) == 1

    psych_ids = {e.id for e in store.living_dossier.psych_profile_index._items}
    assert "core_motivation" in psych_ids
    assert "memory_journal_0" in psych_ids
    assert len(psych_ids) == 7

    ling_ids = {e.id for e in store.living_dossier.linguistic_profile_index._items}
    assert ling_ids == {"vocabulary_syntax", "rhythm_imagery"}
