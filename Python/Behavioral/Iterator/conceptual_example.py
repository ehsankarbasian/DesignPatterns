from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any


"""
We need to implement:
    The __iter__  method in the iterated object (collection)
    The __next__  method in theiterator.
"""


class AlphabeticalOrderIterator(Iterator):
    """
    Implement various traversal algorithms.
    Store the current traversal position at all times.
    """

    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: WordsCollection, reverse: bool = False):
        self._collection = collection
        self._reverse = reverse
        self._sorted_items = None  # Will be set on first __next__ call
        self._position = 0

    def __next__(self) -> Any:
        # Sorting happens only when the first items is actually requested.
        if self._sorted_items is None:
            self._sorted_items = sorted(self._collection._collection)
            if self._reverse:
                self._sorted_items = list(reversed(self._sorted_items))

        if self._position >= len(self._sorted_items):
            raise StopIteration()
        value = self._sorted_items[self._position]
        self._position += 1
        return value


class WordsCollection(Iterable):
    """
    Concrete Collections provide one or several methods for retrieving fresh
    iterator instances, compatible with the collection class.
    """

    def __init__(self, collection: list[Any] | None = None) -> None:
        self._collection = collection or []


    def __getitem__(self, index: int) -> Any:
        return self._collection[index]

    def __iter__(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self)

    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        return AlphabeticalOrderIterator(self, reverse=True)

    def add_item(self, item: Any) -> None:
        self._collection.append(item)


if __name__ == "__main__":
    collection = WordsCollection()
    collection.add_item("B")
    collection.add_item("A")
    collection.add_item("C")
    
    for c in collection:
        print(c)
    
    print()
    for c in collection.get_reverse_iterator():
        print(c)

