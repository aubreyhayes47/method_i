# method_i

This repository hosts design documents for the Method I Narrative Engine. See [ROADMAP.md](ROADMAP.md) for the implementation plan derived from section 8 of the main design document.

## Project Status

Phase 1 delivered the foundational character schemas and the **Living Dossier** system for tracking evolving memories. Phase 2 Task 3 adds the `ScenePipeline`, which consumes dossier data to generate each new scene turn.

- [backend/dossier](backend/dossier/README.md) – how living dossiers feed scene generation.
- [backend/scene](backend/scene/README.md) – pipeline stages for producing dialogue and action.

