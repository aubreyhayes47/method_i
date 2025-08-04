from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple
import time

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

    def run_scene(
        self,
        *,
        max_turns: Optional[int] = None,
        max_duration: Optional[float] = None,
        stop_callback: Optional[Callable[[SceneState], bool]] = None,
    ) -> Tuple[SceneState, str]:
        """Run turns until reaching ``max_turns`` or ``max_duration``.

        Parameters
        ----------
        max_turns:
            Maximum number of turns to execute before stopping.
        max_duration:
            Maximum time in seconds to run before timing out.
        stop_callback:
            Callable evaluated after each turn. If it returns a truthy value,
            the scene stops with reason ``manual_stop``.

        Returns
        -------
        Tuple[SceneState, str]
            Final state and a termination reason of either ``max_turns`` or
            ``timeout``.
        """

        if max_turns is None and max_duration is None:
            raise ValueError("max_turns or max_duration must be provided")

        start_time = time.time()
        turn_count = 0
        termination_reason = ""

        while True:
            if max_turns is not None and turn_count >= max_turns:
                termination_reason = "max_turns"
                break
            if (
                max_duration is not None
                and time.time() - start_time >= max_duration
            ):
                termination_reason = "timeout"
                break

            self.state.turn += 1
            turn_count += 1

            if stop_callback is not None and stop_callback(self.state):
                termination_reason = "manual_stop"
                break

        return self.state, termination_reason

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
