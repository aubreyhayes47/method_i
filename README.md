# method_i

This repository hosts design documents for the Method I Narrative Engine. See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from section 8 of the main design document.

## Project Status

Phase 1 delivered the foundational character schemas and the **Living Dossier** system for tracking evolving memories. Phase 2 Task 3 adds the `ScenePipeline`, which consumes dossier data to generate each new scene turn.

- [backend/dossier](backend/dossier/README.md) – how living dossiers feed scene generation.
- [backend/scene](backend/scene/README.md) – pipeline stages for producing dialogue and action.

## LLM Configuration

Default parameters for LLM calls live in `config/llm.yaml`. The file defines
the provider, model, sampling temperature, and request timeout. Each provider
also includes an `api_key` and `base_url` entry.

`LLMClient.from_config` loads this file and can be overridden via environment
variables or method arguments.

### Environment variables

The client recognises the following variables:

| Variable           | Default                     | Description                     |
| ------------------ | --------------------------- | ------------------------------- |
| `LLM_PROVIDER`     | `openai`                    | Name of the LLM provider.       |
| `LLM_MODEL`        | value from config           | Model used for generation.      |
| `LLM_TEMPERATURE`  | value from config (`0.7`)   | Sampling temperature.           |
| `LLM_TIMEOUT`      | value from config (`30`)    | Request timeout in seconds.     |
| `OPENAI_API_KEY`   | `null`                      | API key for the OpenAI provider.|
| `OPENAI_BASE_URL`  | `https://api.openai.com/v1` | Endpoint for the OpenAI API.    |
| `OLLAMA_BASE_URL`  | `http://localhost:11434`    | Ollama base URL.                |

Provider-specific variables use the pattern `<PROVIDER>_API_KEY` and
`<PROVIDER>_BASE_URL`.

Set these variables in your environment before running code that calls the
LLM.

### Switching providers

Choose a provider with `LLM_PROVIDER` and set any required credentials:

```bash
# OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Local Ollama server
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
```

### Troubleshooting

**OpenAI**

- `401 Unauthorized` – check that `OPENAI_API_KEY` is valid and not expired.
- Connection errors – confirm `OPENAI_BASE_URL` and network access.

**Ollama**

- `Connection refused` – ensure the Ollama server is running at
  `OLLAMA_BASE_URL`.
- `404` or `model not found` – pull the model or verify its name.

## Development Progress (Tasks 2–4)
- **Task 2:** Established the core scene generation loop that retrieves context and constructs prompts.
- **Task 3:** Wired the loop to an LLM backend and validated parsing of model responses.
- **Task 4:** Added configuration flags and basic error handling to guard against malformed LLM output.

## Environment Variables
The pipeline expects the following variables at runtime:

- `OPENAI_API_KEY` – API key for accessing the LLM provider.
- `OLLAMA_BASE_URL` – Base URL for a local Ollama server.
- `LLM_PROVIDER` – Name of the LLM provider (default `openai`).
- `LLM_MODEL` – Model name used for inner monologue and dialogue.
- `LLM_TEMPERATURE` – Sampling temperature for generation.
- `LLM_TIMEOUT` – Request timeout in seconds.
- `SCENE_MAX_TURNS` – Upper bound for automatic scene termination.
- `DB_URL` – Location of the backing store for dossiers and scenes.
