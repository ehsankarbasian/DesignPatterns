from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable, Iterator
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import BinaryTree, Node

from order_strategy import REVERSE_STRATEGY_MAP


class AbstractBaseIterable(Iterable):

    @property
    @abstractmethod
    def iterate_strategy(self) -> Callable[[Optional[Node]], Iterator[Node]]:
        pass

    def __iter__(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self)

    def get_reverse_iterator(self) -> BinaryTreeIterator:
        return BinaryTreeIterator(self, reverse=True)


class BinaryTreeIterator(Iterator):

    def __init__(self, collection: BinaryTree, reverse: bool = False):
        self._collection: BinaryTree = collection
        self._reverse: bool = reverse
        self._generator: Optional[Iterator[Node]] = None

    def __iter__(self) -> BinaryTreeIterator:
        return self

    def __next__(self) -> Node:
        tree = self._collection
        if self._generator is None:
            strategy = tree.iterate_strategy

            if self._reverse:
                strategy = REVERSE_STRATEGY_MAP.get(strategy, strategy)

            self._generator = strategy(tree.root)

        return next(self._generator)
