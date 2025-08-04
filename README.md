# method_i

This repository hosts design documents for the Method I Narrative Engine. See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from section 8 of the main design document.

## Project Status

Phase 1 delivered the foundational character schemas and the **Living Dossier** system for tracking evolving memories. Phase 2 Task 3 adds the `ScenePipeline`, which consumes dossier data to generate each new scene turn.

- [backend/dossier](backend/dossier/README.md) – how living dossiers feed scene generation.
- [backend/scene](backend/scene/README.md) – pipeline stages for producing dialogue and action.

## LLM Configuration

Default parameters for LLM calls live in `config/llm.yaml`. The `LLMClient`
class reads this file to determine the model, temperature, and token
limits. These defaults can be overridden at runtime by passing explicit
values to `LLMClient.generate()`.

### Environment variables

The client expects the following variables to be present:

| Variable         | Purpose                                             |
| ---------------- | --------------------------------------------------- |
| `OPENAI_API_KEY` | API key used when invoking the OpenAI SDK.          |
| `LLM_MODEL`      | *(optional)* Overrides the model defined in the config file. |

Set these variables in your environment before running code that calls the LLM.

## Development Progress (Tasks 2–4)
- **Task 2:** Established the core scene generation loop that retrieves context and constructs prompts.
- **Task 3:** Wired the loop to an LLM backend and validated parsing of model responses.
- **Task 4:** Added configuration flags and basic error handling to guard against malformed LLM output.

## Environment Variables
The pipeline expects the following variables at runtime:
- `OPENAI_API_KEY` – API key for accessing the LLM provider.
- `LLM_MODEL` – Model name used for inner monologue and dialogue.
- `SCENE_MAX_TURNS` – Upper bound for automatic scene termination.
- `DB_URL` – Location of the backing store for dossiers and scenes.
