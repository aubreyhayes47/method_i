from __future__ import annotations
from typing import Dict, Any, List

from living_dossier import LivingDossier


def assemble_context(scene_state: Dict[str, Any], dossier: LivingDossier) -> Dict[str, Any]:
    """Assemble context for the current scene.

    Parameters
    ----------
    scene_state:
        Dictionary containing scene information.  It must include a
        ``character_ids`` key with the list of participating character
        identifiers.
    dossier:
        ``LivingDossier`` instance used for retrieving memories and
        linguistic traits.
    """
    character_ids: List[str] = scene_state.get("character_ids", [])
    memories: Dict[str, List[str]] = {}
    traits: Dict[str, Dict[str, Any]] = {}
    for cid in character_ids:
        memories[cid] = dossier.retrieve_memories(cid)
        traits[cid] = dossier.retrieve_linguistic_traits(cid)

    context = {
        "memories": memories,
        "linguistic_traits": traits,
    }
    return context


def run_pipeline(scene_state: Dict[str, Any], dossier: LivingDossier) -> Dict[str, Any]:
    """Execute the pipeline for a given ``scene_state``.

    This function currently assembles the ``context`` object and returns it.
    In the full system the ``context`` would be supplied to later stages such as
    prompt construction or language model calls.
    """
    context = assemble_context(scene_state, dossier)
    # Placeholder for later stages: e.g. generate dialogue, logging, etc.
    return context
