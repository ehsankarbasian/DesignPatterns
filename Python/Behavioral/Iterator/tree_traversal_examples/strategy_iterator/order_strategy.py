"""
Design goal:
    Define functional tree traversal strategies producing lazy node generators.

Key decisions:
    Model strategies as stateless generator functions conforming to Callable type contracts.
    Support both depth-first variations (pre-order, in-order, post-order) and breadth-first level-order traversal.
    Use collections.deque for efficient O(1) queue operations during breadth-first exploration.

Trade-offs:
    Breadth-first traversal requires O(w) heap memory (proportional to maximum tree width) for queue management.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from binary_tree import BinaryTree

# Functional Strategy Interface
TraversalStrategy = Callable[["BinaryTree"], Generator[Any, None, None]]


# Concrete Strategy: In-Order (DFS)
def in_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in in-order sequence (Left, Root, Right).

    Key decisions:
        Delegate recursion lazily via yield from to maintain minimal call stack frame overhead.

    Trade-offs:
        Deeply unbalanced trees consume call stack proportional to tree height O(h).
    """
    if tree is None:
        return
    yield from in_order_traversal(tree.left_child)
    yield tree.value
    yield from in_order_traversal(tree.right_child)


# Concrete Strategy: Reverse In-Order (DFS)
def reverse_in_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in reverse in-order sequence (Right, Root, Left).

    Key decisions:
        Mirror in-order recursion symmetrically.

    Trade-offs:
        Consumes O(h) call stack memory.
    """
    if tree is None:
        return
    yield from reverse_in_order_traversal(tree.right_child)
    yield tree.value
    yield from reverse_in_order_traversal(tree.left_child)


# Concrete Strategy: Pre-Order / Default DFS
def pre_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in pre-order sequence (Root, Left, Right).

    Key decisions:
        Yield root value before exploring subtree branches.

    Trade-offs:
        Consumes O(h) call stack memory.
    """
    if tree is None:
        return
    yield tree.value
    yield from pre_order_traversal(tree.left_child)
    yield from pre_order_traversal(tree.right_child)


# Concrete Strategy: Reverse Pre-Order (DFS)
def reverse_pre_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in reverse pre-order sequence (Root, Right, Left).

    Key decisions:
        Visit root before exploring right then left branches.

    Trade-offs:
        Consumes O(h) call stack memory.
    """
    if tree is None:
        return
    yield tree.value
    yield from reverse_pre_order_traversal(tree.right_child)
    yield from reverse_pre_order_traversal(tree.left_child)


# Concrete Strategy: Post-Order (DFS)
def post_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in post-order sequence (Left, Right, Root).

    Key decisions:
        Exhaust child subtrees prior to yielding root node value.

    Trade-offs:
        Consumes O(h) call stack memory.
    """
    if tree is None:
        return
    yield from post_order_traversal(tree.left_child)
    yield from post_order_traversal(tree.right_child)
    yield tree.value


# Concrete Strategy: Reverse Post-Order (DFS)
def reverse_post_order_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree in reverse post-order sequence (Right, Left, Root).

    Key decisions:
        Visit right and left subtrees prior to root node evaluation.

    Trade-offs:
        Consumes O(h) call stack memory.
    """
    if tree is None:
        return
    yield from reverse_post_order_traversal(tree.right_child)
    yield from reverse_post_order_traversal(tree.left_child)
    yield tree.value


# Concrete Strategy: Breadth-First Search (BFS / Level-Order)
def breadth_first_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree level by level using a FIFO queue.

    Key decisions:
        Utilize collections.deque to maintain O(1) node enqueue and dequeue latency.
        Yield node value lazily as each element is dequeued.

    Trade-offs:
        Allocates O(w) heap memory where w represents maximum tree width.
    """
    if tree is None:
        return

    queue: deque[BinaryTree] = deque([tree])
    while queue:
        current: BinaryTree = queue.popleft()
        yield current.value
        if current.left_child is not None:
            queue.append(current.left_child)
        if current.right_child is not None:
            queue.append(current.right_child)


# Concrete Strategy: Reverse Breadth-First Search (BFS / Right-to-Left Level-Order)
def reverse_breadth_first_traversal(tree: Optional[BinaryTree]) -> Generator[Any, None, None]:
    """
    Design goal:
        Traverse binary tree level by level from right to left using a FIFO queue.

    Key decisions:
        Enqueue right child prior to left child for each visited node.

    Trade-offs:
        Allocates O(w) heap memory where w represents maximum tree width.
    """
    if tree is None:
        return

    queue: deque[BinaryTree] = deque([tree])
    while queue:
        current: BinaryTree = queue.popleft()
        yield current.value
        if current.right_child is not None:
            queue.append(current.right_child)
        if current.left_child is not None:
            queue.append(current.left_child)
