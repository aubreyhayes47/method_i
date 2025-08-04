# LLM Module

The `backend.llm` package houses utilities for talking to language model
providers.

## Architecture

- `client.py` offers `LLMClient`, a minimal HTTP wrapper with retry and
  exponential backoff. It reads `LLM_API_KEY` and `LLM_API_URL` from the
  environment.
- The repository-level `llm_client.py` builds on this, loading defaults from
  `config/llm.yaml` and exposing a `from_config` constructor that selects
  provider, model, and timeouts.

## Switching providers

`llm_client.LLMClient` chooses a provider from `config/llm.yaml` or the
`LLM_PROVIDER` environment variable. Each provider supplies its own API key and
base URL. To swap backends:

```bash
# OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...

# Local Ollama server
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
```

Provider variables follow the pattern `<PROVIDER>_API_KEY` and
`<PROVIDER>_BASE_URL`, so additional providers can be added by extending the
YAML file and setting matching environment variables.

