"""API endpoints for the casting module."""

from dataclasses import asdict

from fastapi import APIRouter

from .models import CastingCallLogStore


router = APIRouter()

# In-memory store for casting call records
casting_call_log = CastingCallLogStore()


@router.get("/casting-call/candidates")
def get_casting_call_candidates() -> list[dict]:
    """Return all casting call log entries as JSON."""

    return [asdict(log) for log in casting_call_log.all()]

