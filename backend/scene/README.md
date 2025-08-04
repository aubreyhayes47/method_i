# Scene Module

The scene module orchestrates turn-by-turn generation for an active narrative scene.

## LLM Integration
- Retrieves character memories and prior turns to build a prompt for the Large Language Model.
- Sends inner monologue and dialogue prompts to the LLM and applies the structured JSON replies to update scene state.

## Configuration
Environment variables drive LLM behavior:
- `OPENAI_API_KEY` authorizes requests to the model provider.
- `LLM_MODEL` selects the model used for both inner monologue and dialogue generation.
- `SCENE_MAX_TURNS` caps the number of turns before the scene automatically ends.

## Error Handling
- Timeouts or transport errors trigger a retry with exponential backoff.
- Malformed JSON from the LLM is logged and ignored for that turn, preserving the previous scene state.
- All exceptions surface through structured logs so monitoring can alert operators.
