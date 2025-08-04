import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.casting.pipeline import DossierCompiler


class FlakyLLMClient:
    """Return invalid JSON on first call, valid on second."""

    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str):
        self.calls += 1
        if self.calls == 1:
            return {}
        return {"name": "Alice"}


class BadLLMClient:
    """Always return invalid JSON."""

    def __init__(self):
        self.calls = 0

    def generate(self, prompt: str):
        self.calls += 1
        return {}


SCHEMA = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
    "additionalProperties": False,
}


def test_compile_retries_until_valid():
    client = FlakyLLMClient()
    compiler = DossierCompiler(llm_client=client, schema=SCHEMA, max_retries=1)
    result = compiler.compile("prompt")
    assert result == {"name": "Alice"}
    assert client.calls == 2


def test_compile_raises_after_retries():
    client = BadLLMClient()
    compiler = DossierCompiler(llm_client=client, schema=SCHEMA, max_retries=1)
    with pytest.raises(ValueError):
        compiler.compile("prompt")
    assert client.calls == 2
