import os
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.scene.pipeline import ScenePipeline


class DummyClient:
    def complete(self, prompt: str, *, model: str, temperature: float) -> str:
        return "ok"


def test_update_state_adds_dialogue_and_actions():
    pipeline = ScenePipeline(llm_client=DummyClient())
    state = pipeline.update_state(
        dialogue={"speaker": "A", "text": "Hello"}, actions=["wave"]
    )
    assert state.history[-1]["dialogue"]["speaker"] == "A"
    assert state.history[-1]["actions"] == ["wave"]
    assert state.turn == 1
