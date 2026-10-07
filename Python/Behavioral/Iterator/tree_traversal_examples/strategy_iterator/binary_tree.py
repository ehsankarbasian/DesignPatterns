from __future__ import annotations

from collections.abc import Iterator
from typing import Callable, Optional

from iterator import AbstractBaseIterable


# Element (Node)
class Node:
    """
    Design goal:
        Represent a minimal pointer-based binary tree node for lazy traversal.

    Key decisions:
        Use Optional[Node] for explicit nullable parent and child links.
        Enforce single-assignment for children to prevent silent graph rewiring.

    Trade-offs:
        Immutable child links prevent mutation bugs but require tree reconstruction for dynamic re-balancing.
    """

    def __init__(self, node_name: str, parent: Optional[Node] = None) -> None:
        self._name: str = node_name
        self._parent: Optional[Node] = parent
        self._left_child: Optional[Node] = None
        self._right_child: Optional[Node] = None

    @property
    def parent(self) -> Optional[Node]:
        return self._parent

    @property
    def left_child(self) -> Optional[Node]:
        return self._left_child

    @property
    def right_child(self) -> Optional[Node]:
        return self._right_child

    def _add_left_child(self, left_child: Node) -> None:
        """Attach a left child; raises ValueError if already present."""

        if self._left_child is not None:
            raise ValueError("Left child already exists")
        self._left_child = left_child

    def _add_right_child(self, right_child: Node) -> None:
        """Attach a right child; raises ValueError if already present."""

        if self._right_child is not None:
            raise ValueError("Right child already exists")
        self._right_child = right_child

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Node(name={self._name!r})"


# Concrete Aggregate / Strategy Context
class BinaryTree(AbstractBaseIterable):
    """
    Design goal:
        Provide a tree container that delegates traversal to an injected iteration strategy.

    Key decisions:
        Maintain a purely pointer-based hierarchy starting at root without cached node lists.
        Require explicit configuration of iterate_strategy before iteration.

    Trade-offs:
        Strategy indirection enables interchangeable lazy traversals but requires prior setup by client.
    """

    def __init__(self, root_name: str = "root") -> None:
        self._root: Node = Node(node_name=root_name)
        self._iterate_strategy: Optional[Callable[[Optional[Node]], Iterator[Node]]] = None

    @property
    def root(self) -> Node:
        return self._root

    @property
    def iterate_strategy(self) -> Callable[[Optional[Node]], Iterator[Node]]:
        if self._iterate_strategy is None:
            raise ValueError("Iterate strategy has not been set")
        return self._iterate_strategy

    @iterate_strategy.setter
    def iterate_strategy(self, value: Callable[[Optional[Node]], Iterator[Node]]) -> None:
        self._iterate_strategy = value

    def add_left_child(self, name: str, parent: Node) -> Node:
        child = Node(node_name=name, parent=parent)
        parent._add_left_child(child)
        return child

    def add_right_child(self, name: str, parent: Node) -> Node:
        child = Node(node_name=name, parent=parent)
        parent._add_right_child(child)
        return child
