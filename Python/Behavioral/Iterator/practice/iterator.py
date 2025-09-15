from __future__ import annotations
from typing import Any, TYPE_CHECKING

from collections.abc import Iterable, Iterator

if TYPE_CHECKING:
    from binary_tree import BinaryTree, Node


class BaseIterable(Iterable):
    
    def __getitem__(self, index: int):
        return self._collection[index]

    def __iter__(self) -> PreOrderIterator:
        return PreOrderIterator(self)

    def get_reverse_iterator(self) -> PreOrderIterator:
        return PreOrderIterator(self, reverse=True)


class PreOrderIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: BinaryTree, reverse: bool = False):
        self._collection = collection
        self._reverse = reverse
        self._sorted_items = None  # Will be set on first __next__ call
        self._position = 0

    def __next__(self) -> Any:
        # Sorting happens only when the first items is actually requested.
        if self._sorted_items is None:
            root = self._collection._collection[0]
            self._sorted_items = PreOrderIterator._preorder(root)
            if self._reverse:
                self._sorted_items = list(reversed(self._sorted_items))

        if self._position >= len(self._sorted_items):
            raise StopIteration()
        value = self._sorted_items[self._position]
        self._position += 1
        return value
    
    
    @staticmethod
    def _preorder(node: Node, sorted_collection: list[Node] = []):
        if node is None:
            return
        
        sorted_collection.append(node)
        PreOrderIterator._preorder(node.left_child, sorted_collection)
        PreOrderIterator._preorder(node.right_child, sorted_collection)
        
        return sorted_collection
