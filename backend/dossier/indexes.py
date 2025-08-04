from abc import ABC, abstractmethod
from typing import Any, List


class BaseIndex(ABC):
    """Simple interface for index implementations."""

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the index."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> List[Any]:
        """Search the index for items matching the query."""
        raise NotImplementedError


class ListIndex(BaseIndex):
    """Index that stores items in a list and performs keyword search."""

    def __init__(self) -> None:
        self._items: List[Any] = []

    def add(self, item: Any) -> None:
        self._items.append(item)

    def search(self, query: str, top_k: int = 5) -> List[Any]:
        query_lower = query.lower()
        results = [item for item in self._items if query_lower in str(getattr(item, 'content', item)).lower()]
        return results[:top_k]
