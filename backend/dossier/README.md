# Dossier Backend

This directory contains utilities and notes for working with character
dossiers. Currently, the project uses simple in-memory Python data
structures to index and retrieve dossier information. The demo script in
`examples/living_dossier_demo.py` loads
`character_dossier_expanded_method_i.json`, flattens the dossier into an
index, and performs basic keyword searches.

The dossier module manages long-term character memories and traits,
providing grounding data for the scene pipeline. Retrieved memories are
injected into LLM prompts so each turn reflects the character's history
and psychology.

In later development phases, these in-memory structures will be replaced
by a vector database (e.g., Pinecone or FAISS). A vector store will allow
the engine to persist dossier fragments as embeddings and perform
scalable similarity search across characters. When the migration
happens, the indexing logic will be adapted to compute embeddings and
store them in the external vector DB while the retrieval routines will
query the vector store to fetch relevant context for reasoning.

## Integrating with Scene Generation

During scene generation the `ScenePipeline` queries the living dossier of
each participating character:

1. **Retrieve context** – biographical notes, linguistic fingerprints,
   and recent episodic memories are pulled from the dossier's stores.
2. **Construct prompts** – the retrieved fragments feed the inner-
   monologue and dialogue prompts so the model speaks with the
   character's voice and remembers past events.
3. **Persist new memories** – after each turn, the pipeline writes any
   newly created memories back into the dossier, keeping it up to date
   for future scenes.

This feedback loop lets characters evolve as they perform.
