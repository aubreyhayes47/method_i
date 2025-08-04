"""Tests for casting API endpoints."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.casting.api import casting_call_log, router
from backend.casting.models import CharacterCandidate


def test_get_casting_call_candidates_returns_all_logs() -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    casting_call_log._logs.clear()
    casting_call_log.add(CharacterCandidate(name="Jane"))
    casting_call_log.add(CharacterCandidate(name="Tom"), selected=True)

    response = client.get("/casting-call/candidates")
    assert response.status_code == 200
    assert response.json() == [
        {"candidate": {"name": "Jane", "source_chunks": []}, "selected": False},
        {"candidate": {"name": "Tom", "source_chunks": []}, "selected": True},
    ]

