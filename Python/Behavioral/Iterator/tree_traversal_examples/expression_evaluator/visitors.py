from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Generic, TypeVar

from expression_nodes import (
    ExpressionNodeInterface,
    NumberLiteralNode,
    OperatorNode,
)
from traversal import PostOrderTreeIterator

T = TypeVar("T")


# Visitor Interface
class ExpressionVisitorInterface(ABC, Generic[T]):
    """
    Define the operations visitors provide for each concrete expression node.

    Design goal:
        Provide a common visitor interface while retaining result-type flexibility.

    Key decisions:
        - Each concrete node type has a corresponding visit method.
        - Nodes select the appropriate visitor operation through accept.

    Trade-offs:
        Adding a new node type requires extending this interface and updating each
        concrete visitor.
    """

    @abstractmethod
    def visit_literal(self, node: NumberLiteralNode) -> T:
        pass

    @abstractmethod
    def visit_operator(self, node: OperatorNode) -> T:
        pass


# Visitor
class RecursiveEvaluationVisitor(ExpressionVisitorInterface[Decimal]):
    """
    Evaluate expressions recursively through double dispatch.

    Design goal:
        Provide a direct, readable evaluation strategy that follows the expression tree.

    Key decisions:
        - Evaluate child expressions by calling accept recursively.
        - Centralize arithmetic and division-by-zero handling in _apply_operator.

    Trade-offs:
        The implementation closely mirrors the tree structure, but deep trees can
        exceed Python's recursion limit and require nested call-frame state.
    """

    def visit_literal(self, node: NumberLiteralNode) -> Decimal:
        return node.value

    def visit_operator(self, node: OperatorNode) -> Decimal:
        left_value = node.left.accept(self)
        right_value = node.right.accept(self)
        return self._apply_operator(node.operator, left_value, right_value)

    @staticmethod
    def _apply_operator(operator: str, left: Decimal, right: Decimal) -> Decimal:
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == Decimal("0"):
                raise ZeroDivisionError("Division by zero.")
            return left / right

        raise ValueError(f"Unsupported operator: {operator}")


# Visitor
class StackBasedEvaluationVisitor(RecursiveEvaluationVisitor):
    """
    Evaluate post-order nodes iteratively using an explicit operand stack.

    Design goal:
        Avoid recursive evaluation while retaining visitor-based double dispatch.

    Key decisions:
        - Consume nodes from PostOrderTreeIterator.
        - Use accept(self) for dispatch rather than inspecting node types here.
        - Reuse the recursive visitor's operator application logic.
        - Clear operand state at the start of each evaluation.

    Trade-offs:
        Evaluation avoids recursive call-stack limits and stores traversal and operand
        state in heap-allocated lists. In exchange, the visitor must maintain operand
        stack invariants explicitly; overall memory use still depends on tree shape
        and available memory.
    """

    def __init__(self) -> None:
        self._values: list[Decimal] = []

    @property
    def result(self) -> Decimal:
        if len(self._values) != 1:
            raise RuntimeError(
                f"Expected one final value, found {len(self._values)}."
            )
        return self._values[0]

    def visit_literal(self, node: NumberLiteralNode) -> None:
        self._values.append(node.value)

    def visit_operator(self, node: OperatorNode) -> None:
        if len(self._values) < 2:
            raise RuntimeError("Malformed expression: insufficient operands.")

        right_value = self._values.pop()
        left_value = self._values.pop()
        self._values.append(
            self._apply_operator(node.operator, left_value, right_value)
        )

    def evaluate(self, root: ExpressionNodeInterface) -> Decimal:
        self._values.clear()

        for node in PostOrderTreeIterator(root):
            node.accept(self)

        return self.result


# Visitor
class InfixStringVisitor(ExpressionVisitorInterface[str]):
    """
    Render an expression as a fully parenthesized infix string.

    Design goal:
        Show how a second visitor can add a distinct operation without changing
        expression-node classes.

    Key decisions:
        - Recursively render child expressions through accept.
        - Parenthesize each binary operation to preserve its tree grouping.

    Trade-offs:
        The output is unambiguous and easy to inspect, but includes parentheses
        even where operator precedence would make them unnecessary.
    """

    def visit_literal(self, node: NumberLiteralNode) -> str:
        return str(node.value)

    def visit_operator(self, node: OperatorNode) -> str:
        left = node.left.accept(self)
        right = node.right.accept(self)
        return f"({left} {node.operator} {right})"
