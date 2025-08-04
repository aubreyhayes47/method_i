import json
from pathlib import Path
from typing import Dict, Any


def load_dossier(path: str) -> Dict[str, Any]:
    """Load the dossier JSON file into a Python dictionary."""
    return json.loads(Path(path).read_text())


def flatten(data: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten nested dictionaries and lists into a path->value mapping."""
    items: Dict[str, Any] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            items.update(flatten(value, new_prefix))
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            new_prefix = f"{prefix}[{idx}]"
            items.update(flatten(value, new_prefix))
    else:
        items[prefix] = data
    return items


def build_index(dossier: Dict[str, Any]) -> Dict[str, Any]:
    """Create a simple in-memory index from a dossier dictionary."""
    return flatten(dossier)


def search(index: Dict[str, Any], term: str) -> Dict[str, Any]:
    """Search the index for a term in keys or values."""
    term_lower = term.lower()
    return {
        path: value
        for path, value in index.items()
        if term_lower in path.lower()
        or (isinstance(value, str) and term_lower in value.lower())
    }


def main() -> None:
    dossier = load_dossier("character_dossier_expanded_method_i.json")
    index = build_index(dossier)

    # Direct retrieval by path
    path = "properties.blueprint.properties.biographical_summary.type"
    print(f"Value at '{path}': {index.get(path)}")

    # Keyword search demonstration
    term = "gesture"
    results = search(index, term)
    print(f"\nSearch results for '{term}':")
    for k, v in results.items():
        print(f"- {k}: {v}")


if __name__ == "__main__":
    main()
