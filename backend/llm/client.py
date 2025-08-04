from typing import Protocol


class LLMClient(Protocol):
    """Simple protocol representing an LLM client."""

    def complete(self, prompt: str) -> str:  # pragma: no cover - interface
        """Return the model's text response for a given prompt."""
        ...
