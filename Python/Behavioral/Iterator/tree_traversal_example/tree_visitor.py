"""
Composite expression tree with external post-order traversal and visitors.

Design goal:
    Demonstrate how Composite, Visitor, and Iterator work together to represent and
    process arithmetic expressions. Compare recursive evaluation, which follows the
    tree through Python calls, with stack-based evaluation, which consumes an external
    post-order traversal.

Key decisions:
    - Expression nodes dispatch visitor operations through accept.
    - PostOrderTreeIterator traverses the tree lazily using an explicit stack.
    - RecursiveEvaluationVisitor evaluates child expressions recursively.
    - StackBasedEvaluationVisitor processes nodes iteratively through double dispatch
      and maintains an explicit operand stack.

Trade-offs:
    - Recursive evaluation is concise and mirrors the expression structure, but deep
      trees can exceed Python's recursion limit. Each nested call also requires runtime
      call-frame state.
    - Stack-based evaluation avoids recursive calls and their depth limit. Its traversal
      and operand state use heap-allocated lists, but it requires explicit management
      of operand-stack invariants. It does not eliminate memory limits or guarantee
      lower total memory use.

TODO:
    Split this module into expression_nodes.py, visitors.py, and traversal.py.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from decimal import Decimal
import sys
from typing import Generic, TypeVar

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
    def visit_literal(self, node: "NumberLiteralNode") -> T:
        pass

    @abstractmethod
    def visit_operator(self, node: "OperatorNode") -> T:
        pass


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
    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
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

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
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

    def accept(self, visitor: ExpressionVisitorInterface[T]) -> T:
        return visitor.visit_operator(self)

    def __repr__(self) -> str:
        return (
            f"OperatorNode(operator={self._operator!r}, "
            f"left={self._left!r}, right={self._right!r})"
        )


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


if __name__ == "__main__":
    # Build an expression tree representing ((10.50 + 4.50) * 2.00) / (5.00 - 2.00).
    expression = OperatorNode(
        "/",
        OperatorNode(
            "*",
            OperatorNode(
                "+",
                NumberLiteralNode(Decimal("10.50")),
                NumberLiteralNode(Decimal("4.50")),
            ),
            NumberLiteralNode(Decimal("2.00")),
        ),
        OperatorNode(
            "-",
            NumberLiteralNode(Decimal("5.00")),
            NumberLiteralNode(Decimal("2.00")),
        ),
    )

    # Render the expression tree as a fully parenthesized infix string.
    print(expression.accept(InfixStringVisitor()))

    # Evaluate recursively and display the result.
    recursive_result = expression.accept(RecursiveEvaluationVisitor())
    print(f"Recursive result: {recursive_result}")

    # Evaluate the same tree with the post-order iterator and explicit operand stack.
    stack_result = StackBasedEvaluationVisitor().evaluate(expression)
    print(f"Stack-based result: {stack_result}")

    # Verify that both evaluation strategies return the same expected Decimal value.
    assert recursive_result == Decimal("10.00")
    assert stack_result == Decimal("10.00")

    # Build a left-skewed expression tree deeper than the usual Python recursion limit.
    depth = 1200
    deep_expression: ExpressionNodeInterface = NumberLiteralNode(Decimal("1"))

    for _ in range(depth):
        deep_expression = OperatorNode(
            "+",
            deep_expression,
            NumberLiteralNode(Decimal("1")),
        )

    # Demonstrate that recursive evaluation raises RecursionError on this deep tree.
    try:
        deep_expression.accept(RecursiveEvaluationVisitor())
    except RecursionError:
        print(
            f"Recursive evaluation reached the recursion limit "
            f"({sys.getrecursionlimit()})."
        )
    else:
        raise AssertionError(
            "Expected recursive evaluation to raise RecursionError."
        )

    # Verify that stack-based evaluation handles the same deep tree successfully.
    deep_result = StackBasedEvaluationVisitor().evaluate(deep_expression)
    assert deep_result == Decimal("1201")
    print(f"Stack-based deep-tree result: {deep_result}")
