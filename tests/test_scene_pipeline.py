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


def test_run_scene_times_out():
    pipeline = ScenePipeline(llm_client=DummyClient())
    state, reason = pipeline.run_scene(max_duration=0)
    assert reason == "timeout"
    assert state.turn == 0


def test_run_scene_manual_stop():
    pipeline = ScenePipeline(llm_client=DummyClient())

    def stop_after_two(state):
        return state.turn >= 2

    state, reason = pipeline.run_scene(
        max_turns=5, stop_callback=stop_after_two
    )
    assert reason == "manual_stop"
    assert state.turn == 2
