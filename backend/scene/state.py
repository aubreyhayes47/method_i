from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SceneState:
    """Holds the transcript of turns in a scene."""

    transcript: List[Dict[str, str]] = field(default_factory=list)

    def apply_turn(self, turn: Dict[str, str]) -> None:
        """Append a turn to the transcript."""
        self.transcript.append(turn)
