"""
Architecture for expression tree traversal and heterogeneous operations.

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
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import Protocol

    class ExpressionVisitorProtocol(Protocol):
        def visit_literal(self, node: "NumberLiteralNode") -> Any: ...
        def visit_binary_operator(self, node: "BinaryOperatorNode") -> Any: ...


# Component
class AbstractExpressionNode(ABC):
    """Abstract base component representing an expression tree element.

    Design goal:
    Provide a uniform structural interface for all tree elements while enabling
    extensible external operations via double dispatch.

    Key decisions:
    - Enforce accept signature receiving a visitor protocol to decouple nodes
      from concrete visitor implementations.
    - Avoid polluting tree nodes with evaluation or transformation methods.

    Trade-offs:
    - Changes to node types necessitate updating the accept contract across all
      derived elements and visitor protocols.
    """

    @abstractmethod
    def accept(self, visitor: "ExpressionVisitorProtocol") -> Any:
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

    def __init__(self, value: Decimal) -> None:
        self._value: Decimal = value

    @property
    def value(self) -> Decimal:
        return self._value

    def accept(self, visitor: "ExpressionVisitorProtocol") -> Any:
        return visitor.visit_literal(self)

    def __repr__(self) -> str:
        return f"NumberLiteralNode(value={self._value})"


# Composite
class BinaryOperatorNode(AbstractExpressionNode):
    """Composite node representing a binary operation over two child expressions.

    Design goal:
    Model binary arithmetic operations as composite branches connecting left and
    right subtrees.

    Key decisions:
    - Constrain operators to fundamental arithmetic symbols ('+', '-', '*', '/').
    - Expose subtrees as read-only properties to preserve composite structural integrity.
    - Implement accept by calling visit_binary_operator on the supplied visitor.

    Trade-offs:
    - Limited strictly to binary operations; unary expressions require separate modeling.
    """

    SUPPORTED_OPERATORS: frozenset[str] = frozenset({"+", "-", "*", "/"})

    def __init__(
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

    def accept(self, visitor: "ExpressionVisitorProtocol") -> Any:
        return visitor.visit_binary_operator(self)

    def __repr__(self) -> str:
        return (
            f"BinaryOperatorNode(operator='{self._operator}', "
            f"left={self._left}, right={self._right})"
        )
