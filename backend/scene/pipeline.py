from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from .state import SceneState


class LLMClient(Protocol):
    """Protocol for large language model client."""

    def complete(self, prompt: str, *, model: str, temperature: float) -> str:
        """Generate a completion for the given prompt."""


@dataclass
class ScenePipeline:
    """Pipeline that manages state and delegates LLM calls."""

    llm_client: LLMClient
    state: SceneState = field(default_factory=SceneState)

    def update_state(
        self,
        *,
        dialogue: Optional[Dict[str, Any]] = None,
        actions: Optional[List[Any]] = None,
    ) -> SceneState:
        """Merge new dialogue and actions into the state."""

        if dialogue is None and actions is None:
            raise ValueError("update_state requires dialogue or actions")

        entry: Dict[str, Any] = {}

        if dialogue is not None:
            if not isinstance(dialogue, dict):
                raise ValueError("dialogue must be a dict")
            entry["dialogue"] = dialogue

        if actions is not None:
            if not isinstance(actions, list):
                raise ValueError("actions must be a list")
            entry["actions"] = actions

        if not isinstance(self.state.history, list):
            raise ValueError("SceneState.history must be a list")

        self.state.history.append(entry)
        self.state.turn += 1
        return self.state

    def generate_inner_monologue(
        self,
        prompt: str,
        *,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> str:
        """Generate an inner monologue for a character."""

        return self.llm_client.complete(
            prompt, model=model, temperature=temperature
        )

    def generate_dialogue_and_actions(
        self,
        prompt: str,
        *,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ) -> str:
        """Generate dialogue and actions for a scene."""

        return self.llm_client.complete(
            prompt, model=model, temperature=temperature
        )
