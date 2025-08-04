from __future__ import annotations

from typing import Any, Dict, List, Optional

from .state import SceneState


class ScenePipeline:
    """Pipeline that updates and manages the :class:`SceneState`."""

    def __init__(self, state: Optional[SceneState] = None) -> None:
        self.state = state or SceneState()

    def update_state(
        self,
        *,
        dialogue: Optional[Dict[str, Any]] = None,
        actions: Optional[List[Any]] = None,
    ) -> SceneState:
        """Merge new dialogue and actions into the state.

        Parameters
        ----------
        dialogue:
            Mapping describing a dialogue turn, typically with ``speaker`` and
            ``text`` keys.  If provided, it must be a ``dict``.
        actions:
            Sequence of actions that occurred during the turn.  If provided, it
            must be a ``list``.

        Returns
        -------
        SceneState
            The updated state instance.

        Raises
        ------
        ValueError
            If neither ``dialogue`` nor ``actions`` is provided or if either is
            malformed.
        """

        # Basic validation of incoming data
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

        # Ensure history exists
        if not isinstance(self.state.history, list):
            raise ValueError("SceneState.history must be a list")

        self.state.history.append(entry)
        self.state.turn += 1
        return self.state
