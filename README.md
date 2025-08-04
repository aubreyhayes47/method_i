# method_i

This repository hosts design documents for the Method I Narrative Engine. See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from section 8 of the main design document.

## LLM Configuration

Default parameters for LLM calls live in `config/llm.yaml`.
The `LLMClient` class reads this file to determine the model,
temperature, and token limits. These defaults can be overridden at
runtime by passing explicit values to `LLMClient.generate()`.

### Environment variables

The client expects the following variables to be present:

| Variable        | Purpose                                             |
| --------------- | --------------------------------------------------- |
| `OPENAI_API_KEY`| API key used when invoking the OpenAI SDK.          |
| `LLM_MODEL`     | *(optional)* Overrides the model defined in the config file. |

Set these variables in your environment before running code that calls the LLM.

