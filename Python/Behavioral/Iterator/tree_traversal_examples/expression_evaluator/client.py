from decimal import Decimal
import sys

from expression_nodes import (
    ExpressionNodeInterface,
    NumberLiteralNode,
    OperatorNode,
)
from visitors import (
    InfixStringVisitor,
    RecursiveEvaluationVisitor,
    StackBasedEvaluationVisitor,
)

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
