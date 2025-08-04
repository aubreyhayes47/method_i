"""API endpoints for the casting module."""

from dataclasses import asdict
from typing import Callable

from fastapi import APIRouter
from pydantic import BaseModel

from .models import CastingCallLogStore
from .pipeline import DossierCompiler
from ..llm import LLMClient
from ..dossier.models import CharacterStore


router = APIRouter()

# In-memory stores
casting_call_log = CastingCallLogStore()
character_store = CharacterStore()


def _default_compiler() -> DossierCompiler:
    """Create a ``DossierCompiler`` with a fresh ``LLMClient``."""

    return DossierCompiler(llm_client=LLMClient())


# Factory used to obtain a ``DossierCompiler`` instance. Tests may monkeypatch
# this to supply a dummy compiler that avoids real LLM calls.
compiler_factory: Callable[[], DossierCompiler] = _default_compiler


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
    """Compile dossiers for selected candidates.

    For each requested ``candidate_id`` that is marked as selected, run the
    :class:`DossierCompiler`, persist the resulting dossier to
    ``character_store`` and return the compiled summaries.
    """

    logs = casting_call_log.all()
    compiler = compiler_factory()
    compiled: list[dict] = []
    for idx in payload.candidate_ids:
        if 0 <= idx < len(logs) and logs[idx].selected:
            dossier = compiler.compile(logs[idx].candidate)
            character_store.insert(dossier)
            compiled.append(dossier)
    return compiled

