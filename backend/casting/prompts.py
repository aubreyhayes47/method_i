"""Prompt templates for the casting subsystem."""

CASTING_DIRECTOR_PROMPT = (
    "You are a casting director extracting character names from prose. "
    "Given the following text, respond with a JSON object containing a "
    "'characters' list. Each entry must be an object with a 'name' field. "
    "Return only valid JSON.\n\nText:\n"
)
