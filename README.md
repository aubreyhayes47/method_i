# method_i

This repository hosts design documents for the Method I Narrative Engine. See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from section 8 of the main design document.

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
