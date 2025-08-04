from dataclasses import dataclass, field
from typing import Iterable, List, Tuple

from list_index import ListIndex


@dataclass
class LivingDossier:
    """Container for a character's memories and linguistic traits.

    Parameters
    ----------
    memories:
        Iterable of memory strings.
    linguistic_traits:
        Iterable of linguistic trait strings.
    """

    memories: Iterable[str] = field(default_factory=list)
    linguistic_traits: Iterable[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.memory_index = ListIndex(self.memories)
        self.linguistic_trait_index = ListIndex(self.linguistic_traits)

    def retrieve_memories(self, keyword: str) -> List[Tuple[int, str]]:
        """Search ``memories`` for ``keyword`` and return ranked results.

        Delegates to :meth:`ListIndex.search` on the memory index.  The ranking
        score is derived from a naive substring match.

        Parameters
        ----------
        keyword:
            Term to look for.

        Returns
        -------
        List[Tuple[int, str]]
            Tuples of ``(score, memory)`` sorted by ``score`` descending.

        Example
        -------
        >>> dossier = LivingDossier(memories=["Enjoys pizza", "Likes pasta"])
        >>> dossier.retrieve_memories("pizza")
        [(1, 'Enjoys pizza')]

        Notes
        -----
        The underlying search is placeholder logic and should be replaced with
        a more sophisticated ranking algorithm.
        """
        return self.memory_index.search(keyword)

    def retrieve_linguistic_traits(self, keyword: str) -> List[Tuple[int, str]]:
        """Search ``linguistic_traits`` for ``keyword`` and return ranked results.

        Delegates to :meth:`ListIndex.search` on the linguistic trait index.

        Parameters
        ----------
        keyword:
            Term to look for.

        Returns
        -------
        List[Tuple[int, str]]
            Tuples of ``(score, trait)`` sorted by ``score`` descending.

        Example
        -------
        >>> dossier = LivingDossier(linguistic_traits=["uses slang", "formal"])
        >>> dossier.retrieve_linguistic_traits("slang")
        [(1, 'uses slang')]

        Notes
        -----
        The underlying search is placeholder logic and should be replaced with
        a more sophisticated ranking algorithm.
        """
        return self.linguistic_trait_index.search(keyword)
