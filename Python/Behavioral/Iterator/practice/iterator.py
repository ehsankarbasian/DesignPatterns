from __future__ import annotations
from typing import Any, TYPE_CHECKING

from abc import abstractmethod
from collections.abc import Iterable, Iterator

if TYPE_CHECKING:
    from binary_tree import BinaryTree


class AbstractBaseIterable(Iterable):
    
    @property
    @abstractmethod
    def iterate_strategy(self) -> function:
        pass
    
    def __getitem__(self, index: int):
        return self._collection[index]

    def __iter__(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self)

    def get_reverse_iterator(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self, reverse=True)


class BinaryTreeIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: BinaryTree, reverse: bool = False):
        self._collection = collection
        self._reverse = reverse
        self._sorted_items = None  # Will be set on first __next__ call
        self._position = 0

    def __next__(self) -> Any:
        if not hasattr(self._collection, '_iterate_strategy'):
            raise Exception('Set iterate strategy before iterating')
        
        # Sorting happens only when the first items is actually requested.
        if self._sorted_items is None:
            root = self._collection._collection[0]
            self._sorted_items = self._collection.iterate_strategy(root)
            if self._reverse:
                self._sorted_items = list(reversed(self._sorted_items))

        if self._position >= len(self._sorted_items):
            raise StopIteration()
        value = self._sorted_items[self._position]
        self._position += 1
        return value
