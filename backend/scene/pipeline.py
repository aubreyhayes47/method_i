from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class LLMClient(Protocol):
    """Protocol for large language model client."""

    def complete(self, prompt: str, *, model: str, temperature: float) -> str:
        """Generate a completion for the given prompt.

        Implementations should return the raw text response from the model so
        that callers can perform their own JSON parsing or additional
        post-processing.
        """


@dataclass
class ScenePipeline:
    """Coordinates scene generation with an injected :class:`LLMClient`.

    Parameters
    ----------
    llm_client:
        Client used to generate text with a large language model.
    """

    llm_client: LLMClient

    def generate_inner_monologue(
        self,
        prompt: str,
        *,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> str:
        """Generate an inner monologue for a character.

        Parameters
        ----------
        prompt:
            Prompt describing the scene or situation.
        model:
            Name of the model to use for generation.
        temperature:
            Sampling temperature to control randomness.

        Returns
        -------
        str
            Raw text response from the language model.
        """

        response = self.llm_client.complete(
            prompt, model=model, temperature=temperature
        )
        return response

    def generate_dialogue_and_actions(
        self,
        prompt: str,
        *,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> str:
        """Generate a dialogue and corresponding actions for a scene.

        Parameters are identical to :meth:`generate_inner_monologue` and allow
        callers to configure the underlying model invocation.

        Returns
        -------
        str
            Raw text response from the language model.
        """

        response = self.llm_client.complete(
            prompt, model=model, temperature=temperature
        )
        return response
