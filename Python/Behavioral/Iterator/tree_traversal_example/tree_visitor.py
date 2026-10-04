"""
Module-level architecture for expression tree traversal and heterogeneous operations.

Design goal:
Establish a clear separation between structural traversal (Iterator) and
type-specific business operations (Visitor) across an arithmetic expression
composite hierarchy, avoiding fat node interfaces and scattered operation logic.

Key decisions:
- Delegate element navigation to dedicated tree iterators to isolate queue and
  stack traversal mechanics from semantic processing.
- Employ the Visitor pattern with double dispatch to encapsulate multiple
  disparate algorithms (such as decimal evaluation, parenthesized formatting,
  and algebraic constant folding) outside the composite nodes.
- Retain lightweight composite components focused purely on syntax structure
  rather than embedding numerous domain-specific reduction methods.

Trade-offs:
- Simplifies adding new analytical and transformation passes without modifying
  the AST hierarchy.
- Increases system fragility when introducing new expression node variants, as
  all concrete visitors must be updated to satisfy the expanded visitor interface.
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Generic, TypeVar

T = TypeVar("T")


# Visitor Interface
class ExpressionVisitorInterface(ABC, Generic[T]):
    """Pure abstract visitor interface defining double dispatch methods for expression nodes.

    Design goal:
    Provide an abstract contract for heterogeneous operations across all concrete
    variants of the expression composite hierarchy without type mutations.

    Key decisions:
    - Utilize a generic type parameter T to allow concrete visitors to specify
      their distinct computation return types (e.g., Decimal, str, AbstractExpressionNode).
    - Expose explicit visit methods for each concrete expression node variant.

    Trade-offs:
    - Adding a new node class to the composite structure forces updating all
      implementations of this visitor interface.
    """

    @abstractmethod
    def visit_literal(self, node: "NumberLiteralNode") -> T:
        """Process a numeric literal terminal leaf node."""

    @abstractmethod
    def visit_operator(self, node: "OperatorNode") -> T:
        """Process an operator composite branch node."""


# Component
class AbstractExpressionNode(ABC):
    """Abstract base component representing an expression tree element.

    Design goal:
    Provide a uniform structural interface for all tree elements while enabling
    extensible external operations via double dispatch.

    Key decisions:
    - Enforce accept signature receiving a visitor interface to decouple nodes
      from concrete visitor implementations.
    - Avoid polluting tree nodes with evaluation or transformation methods.

    Trade-offs:
    - Changes to node types necessitate updating the accept contract across all
      derived elements and visitor protocols.
    """

    @abstractmethod
    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        """Accept an external visitor and dispatch to its type-specific method."""


# Leaf
class NumberLiteralNode(AbstractExpressionNode):
    """Terminal leaf node holding a constant decimal value.

    Design goal:
    Represent immutable numeric constants within the arithmetic expression
    without evaluating semantics or formatting concerns.

    Key decisions:
    - Enforce Decimal type for precision and compliance with exact numerical invariants.
    - Implement accept by calling visit_literal on the supplied visitor.

    Trade-offs:
    - Requires upfront conversion of numeric inputs to Decimal instances.
    """

    def init(self, value: Decimal) -> None:
        self._value: Decimal = value

    @property
    def value(self) -> Decimal:
        return self._value

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        return visitor.visit_literal(self)

    def repr(self) -> str:
        return f"NumberLiteralNode(value={self._value})"


# Composite
class OperatorNode(AbstractExpressionNode):
    """Composite node representing an arithmetic operation over two child expressions.

    Design goal:
    Model arithmetic operations as composite branches connecting left and
    right operand subtrees.

    Key decisions:
    - Constrain operators to fundamental arithmetic symbols ('+', '-', '*', '/').
    - Expose operand subtrees as read-only properties to preserve composite structural integrity.
    - Implement accept by calling visit_operator on the supplied visitor.

    Trade-offs:
    - Limited strictly to two operands; n-ary expressions require chained nesting.
    """

    SUPPORTED_OPERATORS: frozenset[str] = frozenset({"+", "-", "*", "/"})

    def init(
        self,
        operator: str,
        left: AbstractExpressionNode,
        right: AbstractExpressionNode,
    ) -> None:
        if operator not in self.SUPPORTED_OPERATORS:
            raise ValueError(f"Unsupported operator: {operator}. Expected one of {sorted(self.SUPPORTED_OPERATORS)}")
        self._operator: str = operator
        self._left: AbstractExpressionNode = left
        self._right: AbstractExpressionNode = right

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def left(self) -> AbstractExpressionNode:
        return self._left

    @property
    def right(self) -> AbstractExpressionNode:
        return self._right

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        return visitor.visit_operator(self)

    def repr(self) -> str:
        return (
            f"OperatorNode(operator='{self._operator}', "
            f"left={self._left}, right={self._right})"
        )
