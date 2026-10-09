from collections.abc import Iterator

from expression_nodes import ExpressionNodeInterface, OperatorNode


# Iterator
class PostOrderTreeIterator(Iterator[ExpressionNodeInterface]):
    """
    Yield expression nodes lazily in left-right-operator order.

    Design goal:
        Traverse a composite expression tree without recursive calls.

    Key decisions:
        - Store pending traversal state in an explicit list.
        - Mark operator nodes as expanded before yielding them.
        - Keep structural branching in the iterator, not in evaluation visitors.

    Trade-offs:
        The explicit traversal stack avoids call-stack depth limits, but requires
        bookkeeping to preserve post-order traversal.
    """

    def __init__(self, root: ExpressionNodeInterface) -> None:
        self._stack: list[tuple[ExpressionNodeInterface, bool]] = [(root, False)]

    def __iter__(self) -> "PostOrderTreeIterator":
        return self

    def __next__(self) -> ExpressionNodeInterface:
        while self._stack:
            node, expanded = self._stack.pop()

            if expanded:
                return node

            if isinstance(node, OperatorNode):
                self._stack.append((node, True))
                self._stack.append((node.right, False))
                self._stack.append((node.left, False))
            else:
                return node

        raise StopIteration
