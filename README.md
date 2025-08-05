# Method I: An Introduction to Character-Driven AI

Method I is a revolutionary approach to artificial intelligence and
storytelling that redefines the creative process. At its core, Method I
is a computational dramaturgy engine that directs improvised dramatic
scenes between highly structured, AI-powered Characters.

Instead of simulating a generic human mind, Method I models the specific,
time-tested processes professional actors use to build and perform a
role. This produces characters with depth, believability, and dramatic
potential. Our philosophy is simple: the fundamental unit of creativity
is the **Character**.

## The Method I System: A Two-Part Harmony

The Method I ecosystem comprises two interconnected components:

* **The Method I Acting Training** – a comprehensive system for human
  actors and AI creators to build and inhabit characters.
* **The Method I Narrative Engine** – the technological heart of the
  system, a glass-box architecture that brings characters to life.

### The Two-Phase Character Study Method

The acting training builds a character from the ground up through two
phases.

**Phase I: Character Formation (The Architect's Work)**

This is deep, foundational work: constructing a complete human being
through textual analysis, psychological exploration, and physical
invention.

* **Part A: The Blueprint (Textual Analysis)** – a forensic investigation
  of the character's script to uncover facts, contradictions, and
  linguistic fingerprints.
* **Part B: The Inner World (Psychological & Imaginative Work)** – the
  character's soul, mind, and history, including motivations, fears, and a
  sensory-rich memory journal.
* **Part C: The Physical Form (External Embodiment)** – giving the
  character a distinct, motivated body using techniques like Animal Work
  and the Michael Chekhov Technique.

**Phase II: Scene Grounding (The Actor's Work)**

The practical work used during rehearsal and performance to connect with
the character in the moment.

* **Part A: The Pre-Scene Checklist (Situational Grounding)** – a quick
  mental checklist for focus, presence, and momentum before a scene
  begins.
* **Part B: The In-Scene Activation (Performance Technique)** – actions to
  stay responsive and alive, playing the action and fully engaging the
  senses.

## The Method I Narrative Engine

The Narrative Engine manifests the acting training in technology. It is
a transparent, auditable system that lets creators understand why a
character behaves a certain way.

### Core Components

* **AI Character Dossier** – the digital blueprint of a character,
  containing core data, psychological and linguistic profiles, and
  multimedia assets.
* **Five-Part Generative Chain** – a process that deconstructs performing
  a turn into auditable steps: inner monologue, action and dialogue
  generation, scene analysis, scene closure judgment, and curation.
* **Dramaturgical RAG System** – a context-aware, emotionally informed
  retrieval system that lets characters recall relevant aspects of their
  personality and history.

## The Future Is Character-Driven

Method I shifts how we think about AI and creativity. By treating the
character as the core creative asset, it fosters a future where creators
retain control, characters persist across stories, and creativity becomes
collaborative.

## Repository Overview

This repository hosts design documents for the Method I Narrative Engine.
See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from
section 8 of the main design document.

## Project Status

Phase 1 delivered the foundational character schemas and the **Living Dossier**
system for tracking evolving memories. Phase 2 Task 3 adds the
`ScenePipeline`, which consumes dossier data to generate each new scene turn.
Recent work in the casting module introduced a basic API for reviewing
extracted character candidates.

- [backend/dossier](backend/dossier/README.md) – how living dossiers feed scene
  generation.
- [backend/scene](backend/scene/README.md) – pipeline stages for producing
  dialogue and action.
- [backend/casting](backend/casting/README.md) – extracts characters from source
  texts and exposes candidate logs via an API.

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

## Casting Pipeline

The casting-call pipeline extracts character candidates from source texts
before any scenes are generated. Default settings live in
`config/casting.yaml`:

```yaml
data_source: gutenberg
chunk_strategy: chapter
max_chars_per_chunk: 8000
```

An in-memory `CastingCallLogStore` captures each extracted candidate. A FastAPI
route, `GET /casting-call/candidates`, returns these log entries for review.
Its output seeds the `LivingDossier`, which then supplies the `ScenePipeline`
with character context.

## Scene Configuration

Default scene limits live in `config/scene.yaml`:

```yaml
max_turns: 5
max_duration_seconds: 30
```

`ScenePipeline` loads these settings at start-up. Override them with the
`SCENE_MAX_TURNS` and `SCENE_MAX_DURATION_SECONDS` environment variables or by
supplying ``max_turns`` or ``max_duration_seconds`` when calling
``run_scene``.

### Stop Conditions

Scenes conclude when the turn limit or duration limit is reached, or when a
manual stop is requested. Defaults originate from `config/scene.yaml` and may
be overridden with `SCENE_MAX_TURNS`, `SCENE_MAX_DURATION_SECONDS`, or
equivalent ``run_scene`` arguments.

## Development Progress
- **Task 2:** Established the core scene generation loop that retrieves
  context and constructs prompts.
- **Task 3:** Wired the loop to an LLM backend and validated parsing of model
  responses.
- **Task 4:** Added configuration flags and basic error handling to guard
  against malformed LLM output.
- **Phase 3:** Introduced `GET /casting-call/candidates` for reviewing logged
  character candidates.

## Environment Variables
The pipeline expects the following variables at runtime:

- `OPENAI_API_KEY` – API key for accessing the LLM provider.
- `OLLAMA_BASE_URL` – Base URL for a local Ollama server.
- `LLM_PROVIDER` – Name of the LLM provider (default `openai`).
- `LLM_MODEL` – Model name used for inner monologue and dialogue.
- `LLM_TEMPERATURE` – Sampling temperature for generation.
- `LLM_TIMEOUT` – Request timeout in seconds.
- `SCENE_MAX_TURNS` – Upper bound for automatic scene termination.
- `SCENE_MAX_DURATION_SECONDS` – Maximum time before the scene times out.
- `DB_URL` – Location of the backing store for dossiers and scenes.
