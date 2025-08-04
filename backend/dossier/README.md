# Dossier Module

The dossier subsystem manages character knowledge. Each character has a **LivingDossier** that combines the static blueprint from the character schema with new memories gathered during play.

## Integrating with Scene Generation

During scene generation the `ScenePipeline` queries the living dossier of each participating character:

1. **Retrieve context** – biographical notes, linguistic fingerprints, and recent episodic memories are pulled from the dossier's stores.
2. **Construct prompts** – the retrieved fragments feed the inner‑monologue and dialogue prompts so the model speaks with the character's voice and remembers past events.
3. **Persist new memories** – after each turn, the pipeline writes any newly created memories back into the dossier, keeping it up to date for future scenes.

This feedback loop lets characters evolve as they perform.

