# Casting Module

The `CharacterExtractionPipeline` scans source texts to find characters for new
stories. Extracted names seed the Living Dossier and ultimately inform the
ScenePipeline.

## Pipeline Stages

1. **Fetch Text** – retrieve the full book from a configured source such as
   Project Gutenberg.
2. **Chunk Text** – split the book into segments to keep LLM prompts within
   limits.
3. **Extract Characters** – send each chunk to an LLM to list mentioned
   character names.
4. **Deduplicate** – merge near-duplicate names and record the source chunks for
   provenance.

## Configuration

Default options live in `config/casting.yaml`:

- `data_source` – source for raw books (`gutenberg` by default).
- `chunk_strategy` – splitting method (`chapter` by default).
- `max_chars_per_chunk` – maximum characters per chunk before splitting.

## Integration

The unique candidates produced by this pipeline become initial entries in the
`LivingDossier`. Those dossiers then supply context for the `ScenePipeline`,
ensuring dialogue reflects each character's established background.

## API

An in-memory log tracks candidate reviews and backs two FastAPI routes.
`GET /casting-call/candidates` returns all logged entries as JSON. Use
`POST /casting-call/select` with a JSON body of `{"selected_ids": [...]}` to
mark candidates as selected and receive their updated summaries.
