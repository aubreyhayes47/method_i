import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.casting.pipeline import (
    CharacterExtractionPipeline,
    CastingCallWorkflow,
)
from backend.casting.models import CastingCallLogStore, CharacterCandidate


class DummyLLMClient:
    def generate(self, prompt: str):
        return {"characters": [{"name": "Alice"}, {"name": "Bob"}]}


class DummyPipeline(CharacterExtractionPipeline):
    def fetch_text(self, book_id, source):
        return "text"

    def chunk_text(self, text):
        return [text]


class DummyCompiler:
    def compile(self, candidate: CharacterCandidate, retries: int = 1) -> dict:
        if candidate.name == "Bob":
            return {"name": candidate.name, "error": "fail"}
        return {"name": candidate.name}


def test_workflow_compiles_selected_candidates_and_collects_errors():
    store = CastingCallLogStore()
    extractor = DummyPipeline(llm_client=DummyLLMClient(), store=store)
    compiler = DummyCompiler()
    workflow = CastingCallWorkflow(
        extractor=extractor, compiler=compiler, store=store
    )
    compiled, errors = workflow.run(book_id="123", selected_ids=[0, 1])
    assert compiled == [{"name": "Alice"}]
    assert errors == [{"id": 1, "name": "Bob", "error": "fail"}]
