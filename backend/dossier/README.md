# Dossier Backend

This directory contains utilities and notes for working with character dossiers.
Currently, the project uses simple in-memory Python data structures to index and
retrieve dossier information. The demo script in `examples/living_dossier_demo.py`
loads `character_dossier_expanded_method_i.json`, flattens the dossier into an
index, and performs basic keyword searches.

In later development phases, these in-memory structures will be replaced by a
vector database (e.g., Pinecone or FAISS). A vector store will allow the engine
to persist dossier fragments as embeddings and perform scalable similarity
search across characters. When the migration happens, the indexing logic will be
adapted to compute embeddings and store them in the external vector DB while the
retrieval routines will query the vector store to fetch relevant context for
reasoning.
