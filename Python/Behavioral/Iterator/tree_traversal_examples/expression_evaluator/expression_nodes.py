from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from visitors import ExpressionVisitorInterface

T = TypeVar("T")


# Component
class ExpressionNodeInterface(ABC):
    """
    Define the common double-dispatch interface for expression nodes.

    Design goal:
        Let visitors perform operations on nodes without placing those operations
        inside the node classes.

    Key decisions:
        - Every node implements accept.
        - accept dispatches to the visitor method matching the concrete node type.

    Trade-offs:
        New operations can be added as visitors, but adding a new node type affects
        the visitor interface and its implementations.
    """

    @abstractmethod
    def accept(self, visitor: "ExpressionVisitorInterface[T]") -> T:
        pass


# Leaf
class NumberLiteralNode(ExpressionNodeInterface):
    """
    Represent a decimal constant in the expression tree.

    Design goal:
        Model a leaf value that participates in the same dispatch protocol as
        composite expression nodes.

    Key decisions:
        - Store the value as Decimal.
        - Delegate operation selection to accept through double dispatch.

    Trade-offs:
        Keeping nodes focused on expression structure means evaluation behavior
        resides in visitors rather than in the node.
    """

    def __init__(self, value: Decimal) -> None:
        self._value = value

    @property
    def value(self) -> Decimal:
        return self._value

    def accept(self, visitor: "ExpressionVisitorInterface[T]") -> T:
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"NumberLiteralNode(value={self._value})"


# Composite
class OperatorNode(ExpressionNodeInterface):
    """
    Represent a binary operation with left and right child expressions.

    Design goal:
        Compose expression nodes into a tree while exposing a uniform node interface.

    Key decisions:
        - Hold two child expressions and one supported operator.
        - Validate the operator when constructing the node.
        - Dispatch visitor operations through accept.

    Trade-offs:
        Construction-time validation prevents unsupported operators entering the
        tree, while the fixed supported-operator set requires code changes to extend.
    """

    SUPPORTED_OPERATORS = frozenset({"+", "-", "*", "/"})

    def __init__(
        self,
        operator: str,
        left: ExpressionNodeInterface,
        right: ExpressionNodeInterface,
    ) -> None:
        if operator not in self.SUPPORTED_OPERATORS:
            raise ValueError(f"Unsupported operator: {operator}")

        self._operator = operator
        self._left = left
        self._right = right

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def left(self) -> ExpressionNodeInterface:
        return self._left

    @property
    def right(self) -> ExpressionNodeInterface:
        return self._right

    def accept(self, visitor: "ExpressionVisitorInterface[T]") -> T:
        return visitor.visit_operator(self)

    def __repr__(self) -> str:
        return (
            f"OperatorNode(operator={self._operator!r}, "
            f"left={self._left!r}, right={self._right!r})"
        )
