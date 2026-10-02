from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable, Iterator
from typing import Any, Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import BinaryTree, Node

from order_strategy import REVERSE_STRATEGY_MAP


class AbstractBaseIterable(Iterable):

    @property
    @abstractmethod
    def iterate_strategy(self) -> Callable[[Optional[Node]], Iterator[Node]]:
        pass

    def __getitem__(self, index: int) -> Node:
        return self._collection[index]

    def __iter__(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self)

    def get_reverse_iterator(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self, reverse=True)


class BinaryTreeIterator(Iterator):

    def __init__(self, collection: BinaryTree, reverse: bool = False):
        self._collection = collection
        self._reverse = reverse
        self._generator: Optional[Iterator[Node]] = None

    def __iter__(self) -> BinaryTreeIterator:
        return self

    def __next__(self) -> Node:
        tree = self._collection
        if not hasattr(tree, "_iterate_strategy"):
            raise ValueError("Set iterate strategy before iterating")

        if self._generator is None:
            root = tree.root if hasattr(tree, "root") else tree._collection[0]
            strategy = tree.iterate_strategy

            if self._reverse:
                strategy = REVERSE_STRATEGY_MAP.get(strategy, strategy)

            self._generator = strategy(root)

        return next(self._generator)
