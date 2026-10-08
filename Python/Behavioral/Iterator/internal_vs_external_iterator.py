"""
An executable comparison of external and internal tree iteration.

Trade-offs:
    External iteration gives the client control over traversal timing, early
    stopping, and interleaving with other operations. That flexibility requires
    the client to understand iterator state and the traversal protocol.

    Internal iteration centralizes traversal and keeps simple client code
    concise. The callback controls the operation, not the traversal, so
    pausing, interleaving, or changing traversal flow is less direct.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Generic, List, TypeVar


T = TypeVar("T")


@dataclass
class TreeNode:

    value: str
    children: List["TreeNode"] = field(default_factory=list)


class Tree:

    def __init__(self, root: TreeNode) -> None:
        self._root = root

    @property
    def root(self) -> TreeNode:
        return self._root


class IteratorInterface(ABC, Generic[T]):
    """
    Defines the minimal external iteration contract.

    Trade-offs:
        A small contract keeps concrete traversal implementations replaceable,
        but clients still depend on the semantics of the selected traversal.
    """

    def __iter__(self) -> "IteratorInterface[T]":
        return self

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError


class ExternalTreeIterator(IteratorInterface[TreeNode]):
    """
    Provides client-driven depth-first traversal.

    Pros:
        The client controls when each node is requested and can stop early.
        The iterator follows Python's standard iteration protocol.

    Cons:
        The client must manage iteration control flow manually.
        Traversal state remains allocated across steps until completion.

    Trade-offs:
        This design preserves traversal flexibility at the cost of more
        explicit client interaction and state management.
    """

    def __init__(self, root: TreeNode) -> None:
        self._pending: List[TreeNode] = [root]

    @property
    def has_next(self) -> bool:
        return bool(self._pending)

    def __next__(self) -> TreeNode:
        if not self._pending:
            raise StopIteration

        current = self._pending.pop()
        self._pending.extend(reversed(current.children))
        return current


class InternalTreeIterator:
    """
    Provides collection-driven depth-first traversal through a callback.

    Pros:
        The client only supplies the operation and does not manage traversal
        state. The call site is concise for operations that visit every node.

    Cons:
        The client cannot naturally pause or resume between nodes. Early exit
        requires an additional control protocol or an exception.

    Trade-offs:
        This design makes common traversals easier to express at the cost of
        reducing direct control over traversal timing and flow.
    """

    def __init__(self, root: TreeNode) -> None:
        self._root = root

    def iterate(self, callback: Callable[[TreeNode], None]) -> None:
        pending: List[TreeNode] = [self._root]

        while pending:
            current = pending.pop()
            callback(current)
            pending.extend(reversed(current.children))


if __name__ == "__main__":

    # Build a small sample tree used by both iteration styles.
    tree = Tree(
        TreeNode(
            "root",
            [
                TreeNode("left", [TreeNode("left.leaf")]),
                TreeNode("right"),
            ],
        )
    )

    # External iteration: the client pulls nodes one by one and owns the loop.
    external_iterator = ExternalTreeIterator(tree.root)
    external_values: List[str] = []
    while external_iterator.has_next:
        external_values.append(next(external_iterator).value)

    # Internal iteration: the iterator owns traversal and calls the callback.
    internal_iterator = InternalTreeIterator(tree.root)
    internal_values: List[str] = []
    internal_iterator.iterate(lambda node: internal_values.append(node.value))

    # External iteration example: early stop/search is straightforward for the client.
    search_iterator = ExternalTreeIterator(tree.root)
    found_value = "None"
    while search_iterator.has_next:
        node = next(search_iterator)
        if node.value == "right":
            found_value = node.value
            break

    print("External:", ", ".join(external_values))
    print("Internal:", ", ".join(internal_values))
    print("Found:", found_value)
