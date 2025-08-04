from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Tuple
import os
import time

import yaml

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
    max_turns: Optional[int] = None
    max_duration_seconds: Optional[float] = None
    config_path: str = "config/scene.yaml"

    def __post_init__(self) -> None:
        with open(self.config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        self.max_turns = (
            self.max_turns
            if self.max_turns is not None
            else int(os.getenv("SCENE_MAX_TURNS", cfg.get("max_turns", 1)))
        )
        self.max_duration_seconds = (
            self.max_duration_seconds
            if self.max_duration_seconds is not None
            else float(
                os.getenv(
                    "SCENE_MAX_DURATION_SECONDS",
                    cfg.get("max_duration_seconds", 0),
                )
            )
        )

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
        max_duration_seconds: Optional[float] = None,
    ) -> Tuple[SceneState, str]:
        """Run turns until reaching the supplied limits.

        Parameters
        ----------
        max_turns:
            Maximum number of turns to execute before stopping. Defaults to the
            value loaded from ``config/scene.yaml`` or ``SCENE_MAX_TURNS``.
        max_duration_seconds:
            Maximum time in seconds to run before timing out. Defaults to the
            value loaded from ``config/scene.yaml`` or
            ``SCENE_MAX_DURATION_SECONDS``.

        Returns
        -------
        Tuple[SceneState, str]
            Final state and a termination reason of either ``max_turns`` or
            ``timeout``.
        """

        max_turns = max_turns if max_turns is not None else self.max_turns
        max_duration_seconds = (
            max_duration_seconds
            if max_duration_seconds is not None
            else self.max_duration_seconds
        )

        if max_turns is None and max_duration_seconds is None:
            raise ValueError(
                "max_turns or max_duration_seconds must be provided"
            )

        start_time = time.time()
        turn_count = 0
        termination_reason = ""

        while True:
            if max_turns is not None and turn_count >= max_turns:
                termination_reason = "max_turns"
                break
            if (
                max_duration_seconds is not None
                and time.time() - start_time >= max_duration_seconds
            ):
                termination_reason = "timeout"
                break

            self.state.turn += 1
            turn_count += 1
        final_turn_time = time.time()
        self.state.history.append(
            {
                "event": "final_turn",
                "turn": self.state.turn,
                "timestamp": final_turn_time,
            }
        )
        self.state.terminated = True
        self.state.termination_reason = termination_reason
        self.state.history.append(
            {
                "event": "termination",
                "reason": termination_reason,
                "timestamp": time.time(),
            }
        )

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
