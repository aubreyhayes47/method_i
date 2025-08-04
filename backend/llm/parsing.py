import json

from typing import Any, Dict


class ParseError(ValueError):
    """Raised when an LLM JSON response is invalid."""


REQUIRED_FIELDS = {"dialogue", "action"}


def parse_json_response(text: str) -> Dict[str, Any]:
    """Parse ``text`` as JSON and validate required fields.

    The helper normalises ``actionDescription`` to ``action`` and ensures the
    resulting JSON object contains ``dialogue`` and ``action`` keys.
    ``ParseError`` is raised if parsing fails or if required fields are
    missing.
    """

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ParseError("LLM response must be a JSON object")

    # Allow the model to use actionDescription instead of action
    if "actionDescription" in data and "action" not in data:
        data["action"] = data["actionDescription"]

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ParseError(f"Missing required fields: {', '.join(missing)}")

    return data
