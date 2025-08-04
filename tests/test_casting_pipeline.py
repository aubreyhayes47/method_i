import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.casting.pipeline import CharacterExtractionPipeline
from backend.casting.models import CharacterCandidate


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
