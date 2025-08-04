# Scene Module

The `ScenePipeline` generates each turn of improvisation for the active scene. It coordinates LLM calls and keeps character state synchronized.

## Pipeline Stages

1. **Context Gathering** – pull relevant biography, style, and recent memories from each character's `LivingDossier`.
2. **Inner Monologue** – an LLM call produces the character's hidden intention for the turn.
3. **Dialogue & Action** – a second LLM call generates outward speech and movement using the intention and dossier context.
4. **State Update** – the scene state is updated and any new memories are written back to the dossiers.

The dossier-fed context at the start of the pipeline ensures that every generated line reflects the character's established traits and evolving history.

