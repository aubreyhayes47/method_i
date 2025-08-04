"""Minimal demonstration of a ScenePipeline using random canned responses.

This script defines minimal `SceneState` and `ScenePipeline` classes and runs a
few turns to show how a pipeline might manage state. Responses are selected from
predefined strings so the demo runs without external dependencies. It also
includes a small example of a ``stop_callback`` that could be passed to
``run_scene`` in the full pipeline implementation.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
import random


@dataclass
class SceneState:
    """Simple container for conversation history."""
    history: List[Tuple[str, str]] = field(default_factory=list)


class ScenePipeline:
    """Very small pipeline that appends user input and a canned response."""

    def __init__(self, state: SceneState):
        self.state = state

    def run_turn(self, user_input: str) -> str:
        responses = [
            "Sure, let's continue the adventure.",
            "The scene shifts dramatically.",
            "An unexpected character enters.",
            "A sudden storm changes everything.",
        ]
        response = random.choice(responses)
        self.state.history.append(("user", user_input))
        self.state.history.append(("assistant", response))
        return response


def stop_after_two_turns(state: SceneState) -> bool:
    """Example callback that stops after two user turns."""
    return len(state.history) >= 4


def main() -> None:
    state = SceneState()
    pipeline = ScenePipeline(state)

    for turn in range(3):
        user_input = f"User line {turn + 1}"
        reply = pipeline.run_turn(user_input)
        print(f"Assistant: {reply}")

        if stop_after_two_turns(state):
            print("Stopping early via callback.")
            break

    print("\nConversation history:")
    for speaker, line in state.history:
        print(f"{speaker}: {line}")

    # Demonstrate how a stop callback could be used with the full pipeline.
    from backend.scene.pipeline import ScenePipeline as FullPipeline

    class DummyClient:
        def complete(
            self, prompt: str, *, model: str, temperature: float
        ) -> str:
            return "ok"

    full_pipeline = FullPipeline(llm_client=DummyClient())
    scene_state, reason = full_pipeline.run_scene(
        max_turns=5, stop_callback=stop_after_two_turns
    )
    print(
        f"\nFull pipeline stopped at turn {scene_state.turn} due to {reason}."
    )


if __name__ == "__main__":
    main()
