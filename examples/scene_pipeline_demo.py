"""Minimal demonstration of a ScenePipeline using random canned responses.

This script defines minimal `SceneState` and `ScenePipeline` classes and runs a
few turns to show how a pipeline might manage state. Responses are selected from
predefined strings so the demo runs without external dependencies.
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


def main() -> None:
    state = SceneState()
    pipeline = ScenePipeline(state)

    for turn in range(3):
        user_input = f"User line {turn + 1}"
        reply = pipeline.run_turn(user_input)
        print(f"Assistant: {reply}")

    print("\nConversation history:")
    for speaker, line in state.history:
        print(f"{speaker}: {line}")


if __name__ == "__main__":
    main()
