import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.casting.pipeline import CharacterExtractionPipeline
from backend.casting.models import (
    CharacterCandidate,
    CastingCallLog,
    CastingCallLogStore,
)


class DummyLLMClient:
    def generate(self, prompt: str):
        return {"characters": [{"name": "Alice"}, {"name": "Bob"}]}


def test_extract_characters_parses_candidates():
    pipeline = CharacterExtractionPipeline(llm_client=DummyLLMClient())
    candidates = pipeline.extract_characters(["chunk one", "chunk two"])
    assert candidates == [
        CharacterCandidate(name="Alice", source_chunks=[0]),
        CharacterCandidate(name="Bob", source_chunks=[0]),
        CharacterCandidate(name="Alice", source_chunks=[1]),
        CharacterCandidate(name="Bob", source_chunks=[1]),
    ]


def test_deduplicate_candidates_merges_sources():
    pipeline = CharacterExtractionPipeline(llm_client=DummyLLMClient())
    raw = [
        CharacterCandidate(name="Alice", source_chunks=[0]),
        CharacterCandidate(name="alice", source_chunks=[1]),
        CharacterCandidate(name="Bob", source_chunks=[0]),
    ]
    deduped = pipeline.deduplicate_candidates(raw)
    assert deduped == [
        CharacterCandidate(name="Alice", source_chunks=[0, 1]),
        CharacterCandidate(name="Bob", source_chunks=[0]),
    ]


def test_run_persists_candidates():
    class DummyPipeline(CharacterExtractionPipeline):
        def fetch_text(self, book_id, source):
            return "chunk one\nchunk two"

        def chunk_text(self, text):
            return ["chunk one", "chunk two"]

    store = CastingCallLogStore()
    pipeline = DummyPipeline(llm_client=DummyLLMClient(), store=store)
    result = pipeline.run(book_id="123")

    assert result == [
        CharacterCandidate(
            name="Alice", source_chunks=[0, 1], duplicate=True, minor_role=False
        ),
        CharacterCandidate(
            name="Bob", source_chunks=[0, 1], duplicate=True, minor_role=False
        ),
    ]
    assert store.all() == [
        CastingCallLog(
            candidate=CharacterCandidate(
                name="Alice", source_chunks=[0, 1], duplicate=True, minor_role=False
            ),
            selected=False,
        ),
        CastingCallLog(
            candidate=CharacterCandidate(
                name="Bob", source_chunks=[0, 1], duplicate=True, minor_role=False
            ),
            selected=False,
        ),
    ]


def test_flag_duplicate_candidates_marks_duplicates_and_minor_roles():
    pipeline = CharacterExtractionPipeline(llm_client=DummyLLMClient())
    candidates = [
        CharacterCandidate(name="Alice", source_chunks=[0]),
        CharacterCandidate(name="Bob", source_chunks=[0]),
        CharacterCandidate(name="Charlie", source_chunks=[1, 2]),
    ]
    flagged = pipeline.flag_duplicate_candidates(candidates)
    assert flagged == [
        CharacterCandidate(
            name="Alice", source_chunks=[0], duplicate=True, minor_role=True
        ),
        CharacterCandidate(
            name="Bob", source_chunks=[0], duplicate=True, minor_role=True
        ),
        CharacterCandidate(
            name="Charlie", source_chunks=[1, 2], duplicate=False, minor_role=False
        ),
    ]
