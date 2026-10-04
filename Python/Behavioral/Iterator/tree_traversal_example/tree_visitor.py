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
    """
    Pure abstract visitor interface defining double dispatch methods for expression nodes.

    Design goal:
    Provide an abstract contract for heterogeneous operations across all concrete
    variants of the expression composite hierarchy without type mutations.

    Key decisions:
    - Utilize a generic type parameter T to allow concrete visitors to specify
      their distinct computation return types (e.g., Decimal, str, ExpressionNodeInterface).
    - Expose explicit visit methods for each concrete expression node variant.

    Trade-offs:
    - Adding a new node class to the composite structure forces updating all
      implementations of this visitor interface.
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
    - Enforce accept signature receiving a visitor interface to decouple nodes
      from concrete visitor implementations.
    - Avoid polluting tree nodes with evaluation or transformation methods.

    Trade-offs:
    - Changes to node types necessitate updating the accept contract across all
      derived elements and visitor protocols.
    """

    pass

    @abstractmethod
    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        """Accept an external visitor and dispatch to its type-specific method."""


# Leaf
class NumberLiteralNode(ExpressionNodeInterface):
    """
    Terminal leaf node holding a constant decimal value.

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
class OperatorNode(ExpressionNodeInterface):
    """
    Composite node representing an arithmetic operation over two child expressions.

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

    def repr(self) -> str:
        return (
            f"OperatorNode(operator='{self._operator}', "
            f"left={self._left}, right={self._right})"
        )


# Concrete Visitor: Evaluation
class EvaluationVisitor(ExpressionVisitorInterface[Decimal]):
    """
    Concrete visitor computing the exact decimal evaluation of an expression tree.

    Design goal:
    Evaluate hierarchical arithmetic expressions to a single Decimal value using
    post-order double dispatch traversal without mutating node representations.

    Key decisions:
    - Specialize generic parameter T to Decimal for financial arithmetic precision.
    - Recursively dispatch evaluation through operand accept calls to preserve structural encapsulation.
    - Explicitly guard against division by zero to guarantee deterministic numerical exceptions.

    Trade-offs:
    - Recursive evaluation stack depth scales with tree height, requiring balanced trees for deep expressions.
    """

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
    """
    Concrete visitor generating a fully parenthesized infix string representation of the tree.

    Design goal:
    Produce an unambiguous string representation of an expression tree that explicitly
    reflects evaluation precedence through nested parentheses.

    Key decisions:
    - Specialize generic parameter T to str for textual formatting operations.
    - Wrap binary composite operations in parentheses to maintain structural precedence visually.
    - Format literal numeric values directly to canonical string representations.
Trade-offs:
    - Fully parenthesized output introduces redundant parentheses for associative chains.
    """

    def visit_literal(self, node: NumberLiteralNode) -> str:
        return str(node.value)

    def visit_operator(self, node: OperatorNode) -> str:
        left_expr = node.left.accept(self)
        right_expr = node.right.accept(self)
        return f"({left_expr} {node.operator} {right_expr})"
