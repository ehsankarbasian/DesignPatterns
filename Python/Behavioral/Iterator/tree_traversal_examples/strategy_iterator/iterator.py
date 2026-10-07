from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import BinaryTree, Node

from order_strategy import REVERSE_STRATEGY_MAP, TraversalStrategy


# Aggregate (Iterable)
class AbstractIterable(ABC, Iterable):
    """
    Design goal:
        Provide an abstract base container supporting strategy-driven forward and reverse iteration.

    Key decisions:
        Declare iterate_strategy as an abstract property to enforce explicit traversal strategy binding in subclasses.
        Implement concrete factory methods (__iter__ and get_reverse_iterator) delegating to the private iterator implementation.

    Trade-offs:
        Couples subclasses to the internal _BinaryTreeIterator implementation while simplifying client iteration APIs.
    """

    @property
    @abstractmethod
    def iterate_strategy(self) -> Callable[[Optional[Node]], Iterator[Node]]:
        pass

    def __iter__(self) -> _BinaryTreeIterator:
        return _BinaryTreeIterator(self)

    def get_reverse_iterator(self) -> _BinaryTreeIterator:
        return _BinaryTreeIterator(self, reverse=True)


# Concrete Iterator
class _BinaryTreeIterator(Iterator):
    """
    Design goal:
        Encapsulate stateful iteration over a lazy tree traversal generator.

    Key decisions:
        Keep iterator class private to the module, exposing iteration strictly through the collection interface.
        Lazily evaluate the traversal strategy on the first __next__ invocation.
        Map forward traversal strategies to reverse counterparts via REVERSE_STRATEGY_MAP.

    Trade-offs:
        Lazy generator initialization defers strategy validation until traversal starts instead of construction time.
    """

    def __init__(self, collection: BinaryTree, reverse: bool = False) -> None:
        self._collection: BinaryTree = collection
        self._reverse: bool = reverse
        self._generator: Optional[Iterator[Node]] = None

    def __iter__(self) -> _BinaryTreeIterator:
        return self

    def __next__(self) -> Node:
        if self._generator is None:
            strategy: TraversalStrategy = self._collection.iterate_strategy

            if self._reverse:
                strategy = REVERSE_STRATEGY_MAP.get(strategy, strategy)

            self._generator = strategy(self._collection.root)

        return next(self._generator)
