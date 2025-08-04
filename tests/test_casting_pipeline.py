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
        CharacterCandidate(name="Alice"),
        CharacterCandidate(name="Bob"),
        CharacterCandidate(name="Alice"),
        CharacterCandidate(name="Bob"),
    ]
