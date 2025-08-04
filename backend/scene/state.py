from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class SceneState:
    """Represents the evolving state of a scene.

    Attributes
    ----------
    characters:
        A list of character identifiers present in the scene.
    history:
        Ordered list capturing the dialogue and actions that have occurred.
    turn:
        Integer counter tracking the current turn number.
    terminated:
        Boolean flag indicating whether the scene has concluded.
    termination_reason:
        String describing why the scene ended.
    """

    characters: List[str] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)
    turn: int = 0
    terminated: bool = False
    termination_reason: str = ""
