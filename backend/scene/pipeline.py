from __future__ import annotations

import logging
from typing import Optional

from ..llm.client import LLMClient
from ..llm.parsing import ParseError, parse_json_response
from .state import SceneState


class ScenePipeline:
    """Coordinates LLM calls and updates the scene state."""

    def __init__(self, client: LLMClient, state: SceneState, *, logger: Optional[logging.Logger] = None) -> None:
        self.client = client
        self.state = state
        self.logger = logger or logging.getLogger(__name__)

    def update_state(self, prompt: str) -> dict:
        """Generate a turn and update the scene state.

        On parsing errors a single retry is attempted. If parsing still fails,
        a ``RuntimeError`` is raised and ``SceneState`` remains unchanged.
        """

        response_text = self.client.complete(prompt)
        try:
            parsed = parse_json_response(response_text)
        except ParseError as exc:
            self.logger.warning("LLM parsing failed, retrying once: %s", exc)
            response_text = self.client.complete(prompt)
            try:
                parsed = parse_json_response(response_text)
            except ParseError as exc2:
                self.logger.error("LLM parsing failed after retry: %s", exc2)
                raise RuntimeError("Failed to parse LLM response") from exc2

        self.state.apply_turn(parsed)
        return parsed
