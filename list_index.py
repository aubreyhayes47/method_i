from dataclasses import dataclass, field
from typing import Iterable, List, Tuple


@dataclass
class ListIndex:
    """Simple in-memory index of strings.

    Parameters
    ----------
    items:
        An iterable of strings to index.
    """

    items: Iterable[str] = field(default_factory=list)

    def search(self, keyword: str) -> List[Tuple[int, str]]:
        """Return items containing ``keyword`` ranked by occurrence count.

        The search is intentionally naive and performs a case-insensitive
        substring match.  Each matching item is paired with a score equal to
        the number of times the keyword occurs within that item.

        Parameters
        ----------
        keyword:
            Term to look for within the indexed items.

        Returns
        -------
        List[Tuple[int, str]]
            Tuples of ``(score, item)`` sorted by ``score`` descending.

        Example
        -------
        >>> idx = ListIndex(["I love pizza", "I love pasta"])
        >>> idx.search("pizza")
        [(1, 'I love pizza')]

        Notes
        -----
        This is placeholder logic and should be replaced with a more robust
        search implementation.
        """
        keyword_lower = keyword.lower()
        results: List[Tuple[int, str]] = []
        for item in self.items:
            count = item.lower().count(keyword_lower)
            if count:
                results.append((count, item))
        results.sort(key=lambda x: x[0], reverse=True)
        return results
