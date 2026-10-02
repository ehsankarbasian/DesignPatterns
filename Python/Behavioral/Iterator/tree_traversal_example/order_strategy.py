from __future__ import annotations

from collections.abc import Iterator
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import Node

"""
Design goal:
    Provide a collection of stateless, lazy-evaluating traversal strategies for binary trees.

Key decisions:
    Use generator functions to achieve O(h) space complexity during traversal.
    Define strategies as standalone callables that can be injected into BinaryTree.

Trade-offs:
    Functional strategies offer extreme simplicity and low overhead, but prevent 
    storing internal traversal state (e.g., node path tracking) without external closures.
"""


# Type alias / Strategy Interface
TraversalStrategy = Callable[[Optional["Node"]], Iterator["Node"]]


# Concrete Strategies

def pre_order(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield node
    yield from pre_order(node.left_child)
    yield from pre_order(node.right_child)


def pre_order_reverse(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield from pre_order_reverse(node.right_child)
    yield from pre_order_reverse(node.left_child)
    yield node


def in_order(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield from in_order(node.left_child)
    yield node
    yield from in_order(node.right_child)


def in_order_reverse(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield from in_order_reverse(node.right_child)
    yield node
    yield from in_order_reverse(node.left_child)


def post_order(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield from post_order(node.left_child)
    yield from post_order(node.right_child)
    yield node


def post_order_reverse(node: Optional[Node]) -> Iterator[Node]:
    if node is None:
        return
    yield node
    yield from post_order_reverse(node.right_child)
    yield from post_order_reverse(node.left_child)


REVERSE_STRATEGY_MAP: dict[TraversalStrategy, TraversalStrategy] = {
    pre_order: pre_order_reverse,
    in_order: in_order_reverse,
    post_order: post_order_reverse,
}
