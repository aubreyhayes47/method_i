"""Tests for casting API endpoints."""

import os
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Ensure the repository root is on the import path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.casting.api import casting_call_log, router
from backend.casting.models import CharacterCandidate


@pytest.fixture
def client() -> TestClient:
    """Create a test client with the casting router registered."""

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_log() -> None:
    """Clear the in-memory casting call log before each test."""

    casting_call_log._logs.clear()


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


def test_compile_only_processes_selected_ids(client: TestClient) -> None:
    """Compilation processes only candidates marked as selected."""

    add_candidates()
    client.post("/casting-call/select", json={"selected_ids": [0, 2]})

    response = client.post(
        "/casting-call/compile", json={"candidate_ids": [0, 1, 2]}
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Jane",
            "source_chunks": [],
            "duplicate": False,
            "minor_role": False,
        },
        {
            "name": "Lucy",
            "source_chunks": [],
            "duplicate": False,
            "minor_role": False,
        },
    ]

