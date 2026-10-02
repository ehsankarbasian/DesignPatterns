from __future__ import annotations

from collections.abc import Iterator
from typing import Callable, Optional

from iterator import AbstractBaseIterable


class Node:

    def __init__(self, node_name: str, parent: Optional[Node] = None):
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
        if self._left_child is not None:
            raise ValueError("Left child already exists")
        self._left_child = left_child

    def _add_right_child(self, right_child: Node) -> None:
        if self._right_child is not None:
            raise ValueError("Right child already exists")
        self._right_child = right_child

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Node(name={self._name!r})"


class BinaryTree(AbstractBaseIterable):

    def __init__(self, root_name: str = "root"):
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
