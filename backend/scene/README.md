# Scene Module

The `ScenePipeline` generates each turn of improvisation for the active
scene. It coordinates LLM calls and keeps character state synchronized.

## Pipeline Stages

1. **Context Gathering** – pull relevant biography, style, and recent
   memories from each character's `LivingDossier`.
2. **Inner Monologue** – an LLM call produces the character's hidden
   intention for the turn.
3. **Dialogue & Action** – a second LLM call generates outward speech and
   movement using the intention and dossier context.
4. **State Update** – the scene state is updated and any new memories are
   written back to the dossiers.

The dossier-fed context at the start of the pipeline ensures that every
generated line reflects the character's established traits and evolving
history.

## LLM Integration
- Retrieves character memories and prior turns to build a prompt for the Large Language Model.
- Sends inner monologue and dialogue prompts to the LLM and applies the structured JSON replies to update scene state.

## Configuration
Default scene limits live in `config/scene.yaml`. `ScenePipeline` reads this
file at start-up. Override these values via environment variables or direct
arguments to ``run_scene``:

- `OPENAI_API_KEY` authorizes requests to the model provider.
- `LLM_MODEL` selects the model used for both inner monologue and dialogue
  generation.
- `SCENE_MAX_TURNS` caps the number of turns before the scene automatically
  ends.
- `SCENE_MAX_DURATION_SECONDS` sets a timeout for the entire scene.

## Error Handling
- Timeouts or transport errors trigger a retry with exponential backoff.
- Malformed JSON from the LLM is logged and ignored for that turn, preserving the previous scene state.
- All exceptions surface through structured logs so monitoring can alert operators.
