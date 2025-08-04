"""Tests for casting API endpoints."""

import os
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Ensure the repository root is on the import path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.casting.api import casting_call_log, router, character_store
from backend.casting.models import CharacterCandidate


@pytest.fixture
def client() -> TestClient:
    """Create a test client with the casting router registered."""

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_state() -> None:
    """Clear in-memory stores before each test."""

    casting_call_log._logs.clear()
    character_store._characters.clear()


def add_candidates() -> None:
    """Populate the log with sample candidates."""

    casting_call_log.add(CharacterCandidate(name="Jane"))
    casting_call_log.add(CharacterCandidate(name="Tom"))
    casting_call_log.add(CharacterCandidate(name="Lucy"))


def test_get_casting_call_candidates_returns_all_logs(client: TestClient) -> None:
    """The candidates endpoint returns all logged entries."""

    add_candidates()
    response = client.get("/casting-call/candidates")
    assert response.status_code == 200
    assert response.json() == [
        {
            "candidate": {
                "name": "Jane",
                "source_chunks": [],
                "duplicate": False,
                "minor_role": False,
            },
            "selected": False,
        },
        {
            "candidate": {
                "name": "Tom",
                "source_chunks": [],
                "duplicate": False,
                "minor_role": False,
            },
            "selected": False,
        },
        {
            "candidate": {
                "name": "Lucy",
                "source_chunks": [],
                "duplicate": False,
                "minor_role": False,
            },
            "selected": False,
        },
    ]


def test_select_casting_call_candidates_updates_selection(
    client: TestClient,
) -> None:
    """Selection endpoint marks specified candidates as selected."""

    add_candidates()
    response = client.post(
        "/casting-call/select", json={"selected_ids": [0, 2]}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "candidate": {
                "name": "Jane",
                "source_chunks": [],
                "duplicate": False,
                "minor_role": False,
            },
            "selected": True,
        },
        {
            "candidate": {
                "name": "Lucy",
                "source_chunks": [],
                "duplicate": False,
                "minor_role": False,
            },
            "selected": True,
        },
    ]

    assert [log.selected for log in casting_call_log.all()] == [True, False, True]


def test_compile_generates_dossiers_for_selected_ids(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Compilation generates dossiers and stores them."""

    add_candidates()
    client.post("/casting-call/select", json={"selected_ids": [0, 2]})

    class DummyCompiler:
        def compile(self, candidate, retries: int = 1) -> dict:
            return {
                "name": candidate.name,
                "summary": f"{candidate.name} dossier",
            }

    monkeypatch.setattr(
        "backend.casting.api.compiler_factory", lambda: DummyCompiler()
    )

    response = client.post(
        "/casting-call/compile", json={"candidate_ids": [0, 1, 2]}
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "Jane", "summary": "Jane dossier"},
        {"name": "Lucy", "summary": "Lucy dossier"},
    ]

    stored = [char.dossier for char in character_store.all()]
    assert stored == [
        {"name": "Jane", "summary": "Jane dossier"},
        {"name": "Lucy", "summary": "Lucy dossier"},
    ]

