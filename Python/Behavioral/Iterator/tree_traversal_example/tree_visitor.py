"""
Module-level architecture for expression tree traversal and heterogeneous operations.

Design goal:
    Establish a clear separation between structural traversal (Iterator) and
    type-specific operations (Visitor) across an arithmetic expression composite
    hierarchy, avoiding fat node interfaces.

Key decisions:
    - Employ the Visitor pattern with double dispatch to encapsulate multiple
      disparate algorithms outside the composite nodes.
    - Retain lightweight composite components focused purely on syntax structure.

Trade-offs:
    - Simplifies adding new tree passes without modifying composite classes.
    - Adding new node types forces updating all concrete visitor implementations.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Generic, TypeVar

T = TypeVar("T")


# Visitor Interface
class ExpressionVisitorInterface(ABC, Generic[T]):
    """
    Pure abstract visitor interface defining double dispatch methods for expression nodes.

    Design goal:
        Provide a uniform visitor contract across all expression composite variants.

    Key decisions:
        - Utilize generic parameter T to allow concrete visitors to define specific return types.
        - Expose explicit visit methods for each concrete expression node variant.
    """

    pass

    @abstractmethod
    def visit_literal(self, node: "NumberLiteralNode") -> T:
        """Process a numeric literal terminal leaf node."""

    @abstractmethod
    def visit_operator(self, node: "OperatorNode") -> T:
        """Process an operator composite branch node."""


# Component Interface
class ExpressionNodeInterface(ABC):
    """
    Pure abstract component interface representing an expression tree element.

    Design goal:
        Provide a uniform structural interface for all tree elements while enabling
        extensible external operations via double dispatch.

    Key decisions:
        - Enforce an accept signature to decouple nodes from concrete visitors.
    """

    pass

    @abstractmethod
    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        """Accept an external visitor and dispatch to its type-specific method."""


# Leaf
class NumberLiteralNode(ExpressionNodeInterface):
    """Terminal leaf node holding a constant decimal value."""

    def __init__(self, value: Decimal) -> None:
        self._value: Decimal = value

    @property
    def value(self) -> Decimal:
        return self._value

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"NumberLiteralNode(value={self._value})"


# Composite
class OperatorNode(ExpressionNodeInterface):
    """Composite node representing an arithmetic operation over two child expressions."""

    SUPPORTED_OPERATORS: frozenset[str] = frozenset({"+", "-", "*", "/"})

    def __init__(
        self,
        operator: str,
        left: ExpressionNodeInterface,
        right: ExpressionNodeInterface,
    ) -> None:
        if operator not in self.SUPPORTED_OPERATORS:
            raise ValueError(
                f"Unsupported operator: {operator}. Expected one of {sorted(self.SUPPORTED_OPERATORS)}"
            )
        self._operator: str = operator
        self._left: ExpressionNodeInterface = left
        self._right: ExpressionNodeInterface = right

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def left(self) -> ExpressionNodeInterface:
        return self._left

    @property
    def right(self) -> ExpressionNodeInterface:
        return self._right

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        return visitor.visit_operator(self)

    def __repr__(self) -> str:
        return (
            f"OperatorNode(operator='{self._operator}', "
            f"left={self._left}, right={self._right})"
        )


# Concrete Visitor: Evaluation
class EvaluationVisitor(ExpressionVisitorInterface[Decimal]):
    """Calculates the exact decimal evaluation of an expression tree via post-order dispatch."""

    def visit_literal(self, node: NumberLiteralNode) -> Decimal:
        return node.value

    def visit_operator(self, node: OperatorNode) -> Decimal:
        left_value = node.left.accept(self)
        right_value = node.right.accept(self)

        operator = node.operator
        if operator == "+":
            return left_value + right_value
        if operator == "-":
            return left_value - right_value
        if operator == "*":
            return left_value * right_value
        if operator == "/":
            if right_value == Decimal("0"):
                raise ZeroDivisionError("Division by zero encountered during tree evaluation.")
            return left_value / right_value

        raise ValueError(f"Unknown operator: {operator}")


# Concrete Visitor: Infix String Representation
class InfixStringVisitor(ExpressionVisitorInterface[str]):
    """Produces a fully parenthesized infix string representation from an expression tree."""

    def visit_literal(self, node: NumberLiteralNode) -> str:
        return str(node.value)

    def visit_operator(self, node: OperatorNode) -> str:
        left_expr = node.left.accept(self)
        right_expr = node.right.accept(self)
        return f"({left_expr} {node.operator} {right_expr})"
