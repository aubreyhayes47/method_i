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


def test_run_scene_respects_max_turns():
    pipeline = ScenePipeline(llm_client=DummyClient())
    state, reason = pipeline.run_scene(max_turns=3)
    assert reason == "max_turns"
    assert state.turn == 3
    assert state.terminated is True
    assert state.termination_reason == "max_turns"
    assert state.history[-2]["event"] == "final_turn"
    assert state.history[-2]["turn"] == 3
    assert "timestamp" in state.history[-2]
    assert state.history[-1]["event"] == "termination"
    assert state.history[-1]["reason"] == "max_turns"
    assert "timestamp" in state.history[-1]


def test_run_scene_times_out():
    pipeline = ScenePipeline(llm_client=DummyClient())
    state, reason = pipeline.run_scene(max_duration=0)
    assert reason == "timeout"
    assert state.turn == 0
    assert state.terminated is True
    assert state.termination_reason == "timeout"
    assert state.history[-2]["event"] == "final_turn"
    assert state.history[-2]["turn"] == 0
    assert "timestamp" in state.history[-2]
    assert state.history[-1]["event"] == "termination"
    assert state.history[-1]["reason"] == "timeout"
    assert "timestamp" in state.history[-1]
