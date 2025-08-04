"""API endpoints for the casting module."""

from dataclasses import asdict

from fastapi import APIRouter
from pydantic import BaseModel

from .models import CastingCallLogStore


router = APIRouter()

# In-memory store for casting call records
casting_call_log = CastingCallLogStore()


@router.get("/casting-call/candidates")
def get_casting_call_candidates() -> list[dict]:
    """Return all casting call log entries as JSON."""

    return [asdict(log) for log in casting_call_log.all()]


class SelectionPayload(BaseModel):
    """Payload specifying which candidates were selected."""

    selected_ids: list[int]


@router.post("/casting-call/select")
def select_casting_call_candidates(payload: SelectionPayload) -> list[dict]:
    """Mark candidates as selected and return their summaries.

    The ``selected_ids`` field contains indices into the casting call log. Any
    candidate whose index appears in that list is marked as selected; all others
    are cleared. The updated summaries for the selected candidates are returned
    for confirmation.
    """

    logs = casting_call_log.all()
    selected_summaries = []
    selected_set = set(payload.selected_ids)
    for idx, log in enumerate(logs):
        if idx in selected_set:
            log.selected = True
            selected_summaries.append(asdict(log))
        else:
            log.selected = False
    return selected_summaries


class CompilePayload(BaseModel):
    """Payload specifying candidate IDs to compile."""

    candidate_ids: list[int]


@router.post("/casting-call/compile")
def compile_casting_call_candidates(payload: CompilePayload) -> list[dict]:
    """Return summaries for selected candidates slated for compilation."""

    logs = casting_call_log.all()
    compiled: list[dict] = []
    for idx in payload.candidate_ids:
        if 0 <= idx < len(logs) and logs[idx].selected:
            compiled.append(asdict(logs[idx].candidate))
    return compiled

