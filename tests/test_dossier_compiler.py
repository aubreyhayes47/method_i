import pytest
import jsonschema

from backend.casting.pipeline import DossierCompiler
from backend.casting.models import CharacterCandidate


class DummyLLM:
    def __init__(self, outputs):
        self.outputs = outputs
        self.index = 0

    def generate(self, prompt: str):
        result = self.outputs[self.index]
        if self.index < len(self.outputs) - 1:
            self.index += 1
        return result


def test_compile_retries_and_returns_valid(monkeypatch):
    compiler = DossierCompiler(llm_client=DummyLLM([
        {"invalid": True},
        {"valid": True},
    ]))

    def fake_validate(instance, schema):
        if instance.get("invalid"):
            raise jsonschema.ValidationError("invalid")

    monkeypatch.setattr(
        "backend.casting.pipeline.jsonschema.validate", fake_validate
    )

    result = compiler.compile(CharacterCandidate(name="Alice", source_chunks=[]))
    assert result == {"valid": True}


def test_compile_raises_after_failures(monkeypatch):
    compiler = DossierCompiler(llm_client=DummyLLM([
        {"invalid": True},
        {"invalid": True},
    ]))

    def always_fail(instance, schema):
        raise jsonschema.ValidationError("invalid")

    monkeypatch.setattr(
        "backend.casting.pipeline.jsonschema.validate", always_fail
    )

    candidate = CharacterCandidate(name="Bob", source_chunks=[])
    with pytest.raises(ValueError):
        compiler.compile(candidate)
