# AGENTS Instructions

This repository stores design documents and JSON schemas for the Method I Narrative Engine.

## Style
- Markdown files use `#`-based headings and wrap lines around 80 characters when practical.
- JSON documents use two-space indentation and conform to JSON Schema Draft-07.

## Testing
Before committing changes, run the following from the repository root:

1. **Validate JSON schemas**
   ```bash
   python -m jsonschema -i character_dossier_expanded_method_i.json https://json-schema.org/draft-07/schema
   ```
2. **Run Python tests**
   ```bash
   pytest
   ```

## Pull Requests
- Summarize changes clearly.
- Include snippets of the test command outputs in the PR description.
