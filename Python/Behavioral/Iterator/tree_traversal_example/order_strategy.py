from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import Node


def pre_order(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield node
    yield from pre_order(node.left_child)
    yield from pre_order(node.right_child)


def pre_order_reverse(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield node
    yield from pre_order_reverse(node.right_child)
    yield from pre_order_reverse(node.left_child)


def in_order(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield from in_order(node.left_child)
    yield node
    yield from in_order(node.right_child)


def in_order_reverse(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield from in_order_reverse(node.right_child)
    yield node
    yield from in_order_reverse(node.left_child)


def post_order(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield from post_order(node.left_child)
    yield from post_order(node.right_child)
    yield node


def post_order_reverse(node: Node | None) -> Iterator[Node]:
    if node is None:
        return
    yield from post_order_reverse(node.right_child)
    yield from post_order_reverse(node.left_child)
    yield node
