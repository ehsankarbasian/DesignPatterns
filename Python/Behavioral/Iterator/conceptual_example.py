"""
Design goal:
    Illustrate the foundational Gang of Four Iterator pattern structure using Python iteration protocols.

Key decisions:
    Encapsulate alphabetical sorting mechanics inside a dedicated concrete iterator.
    Defer sorting computation lazily to the initial __next__ invocation.
    Expose forward and reverse iterator factory methods on the aggregate collection.

Trade-offs:
    Sorting the backing list eagerly on the first iterator call incurs an O(N log N) time and O(N) space overhead.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Optional


# Concrete Iterator
class AlphabeticalOrderIterator(Iterator):
    """
    Design goal:
        Provide sequential alphabetical traversal state management over an aggregate collection.

    Key decisions:
        Lazily sort the target collection elements on the first item traversal request.
        Support forward and reverse traversal via an internal direction flag.

    Trade-offs:
        Maintains an internal duplicate sorted slice, doubling memory consumption for the iteration lifespan.
    """

    def __init__(self, collection: WordsCollection, reverse: bool = False) -> None:
        self._collection: WordsCollection = collection
        self._reverse: bool = reverse
        self._sorted_items: Optional[list[Any]] = None
        self._position: int = 0

    def __next__(self) -> Any:
        if self._sorted_items is None:
            self._sorted_items = sorted(self._collection)
            if self._reverse:
                self._sorted_items = list(reversed(self._sorted_items))

        if self._position >= len(self._sorted_items):
            raise StopIteration()

        value: Any = self._sorted_items[self._position]
        self._position += 1
        return value


# Concrete Aggregate
class WordsCollection(Iterable):
    """
    Design goal:
        Store elements and produce compatible iterators conforming to Python Iterable protocol.

    Key decisions:
        Delegate ordering and traversal logic entirely to AlphabeticalOrderIterator instances.
        Provide dedicated factory methods for both forward and reverse iterators.

    Trade-offs:
        Directly relies on an internal list representation rather than a generalized abstract collection contract.
    """

    def __init__(self, collection: Optional[list[Any]] = None) -> None:
        self._collection: list[Any] = collection or []

    def __getitem__(self, index: int) -> Any:
        return self._collection[index]

    def __iter__(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self, reverse=True)

    def add_item(self, item: Any) -> None:
        self._collection.append(item)


# Client
if __name__ == "__main__":
    collection = WordsCollection()
    collection.add_item("B")
    collection.add_item("A")
    collection.add_item("C")

    for item in collection:
        print(item)

    print()
    for item in collection.get_reverse_iterator():
        print(item)
