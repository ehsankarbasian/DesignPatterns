"""
Problem Statement:
In enterprise systems, business rules are often modeled as combinable logical
expressions (e.g., checking if a value is positive, even, or exceeds a threshold)
using domain specifications that can be combined via boolean logic (AND, OR, NOT).

The business requires generating a natural, human-readable Persian description
of these composed business rules (e.g., for audit trails, reporting, UI labels,
or regulatory explanations).

The core challenge is:
How can we generate formatted linguistic representations of complex rule trees
without polluting the domain specification classes with presentation, parsing,
or localization concerns, while maintaining proper operator precedence and parentheses?
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List


# Visitee
class SpecificationInterface(ABC):
    """
    Component Interface in the Composite Pattern and Visitee in the Visitor Pattern.
    Defines the domain specification contract and the double dispatch accept method.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        """Evaluates whether the candidate satisfies the domain specification rule."""
        pass

    @abstractmethod
    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        """First dispatch: accepts a visitor and delegates execution based on runtime type."""
        pass

    def and_(self, other: SpecificationInterface) -> SpecificationInterface:
        return AndSpecification(self, other)

    def or_(self, other: SpecificationInterface) -> SpecificationInterface:
        return OrSpecification(self, other)

    def not_(self) -> SpecificationInterface:
        return NotSpecification(self)


# Visitee
class PositiveSpecification(SpecificationInterface):
    """Leaf Visitee representing a rule checking for strictly positive numbers."""

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > 0

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_positive(self)


# Visitee
class EvenSpecification(SpecificationInterface):
    """Leaf Visitee representing a rule checking for even numbers."""

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate % 2 == 0

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_even(self)


# Visitee
class GreaterThanSpecification(SpecificationInterface):
    """
    Leaf Visitee with encapsulated threshold state.
    Exposes a public getter to allow visitors to format or compile rules
    without directly mutating or violating strict internal encapsulation.
    """

    def __init__(self, threshold: int) -> None:
        self._threshold = threshold

    @property
    def threshold(self) -> int:
        return self._threshold

    def is_satisfied_by(self, candidate: int) -> bool:
        return candidate > self._threshold

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_greater_than(self)


# Visitee
class AndSpecification(SpecificationInterface):
    """
    Composite Visitee representing logical conjunction (AND).
    Holds left and right child specifications.
    """

    def __init__(self, left: SpecificationInterface, right: SpecificationInterface) -> None:
        self._left = left
        self._right = right

    @property
    def left(self) -> SpecificationInterface:
        return self._left

    @property
    def right(self) -> SpecificationInterface:
        return self._right

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_and(self)


# Visitee
class OrSpecification(SpecificationInterface):
    """
    Composite Visitee representing logical disjunction (OR).
    Holds left and right child specifications.
    """

    def __init__(self, left: SpecificationInterface, right: SpecificationInterface) -> None:
        self._left = left
        self._right = right

    @property
    def left(self) -> SpecificationInterface:
        return self._left

    @property
    def right(self) -> SpecificationInterface:
        return self._right

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_or(self)


# Visitee
class NotSpecification(SpecificationInterface):
    """
    Composite Visitee representing logical negation (NOT).
    Holds a single wrapped specification.
    """

    def __init__(self, operand: SpecificationInterface) -> None:
        self._operand = operand

    @property
    def operand(self) -> SpecificationInterface:
        return self._operand

    def is_satisfied_by(self, candidate: Any) -> bool:
        return not self._operand.is_satisfied_by(candidate)

    def accept(self, visitor: SpecificationVisitorInterface) -> None:
        visitor.visit_not(self)


# Visitor
class SpecificationVisitorInterface(ABC):
    """
    Visitor Interface declaring visiting operations for each concrete specification type.
    """

    @abstractmethod
    def visit_positive(self, spec: PositiveSpecification) -> None:
        pass

    @abstractmethod
    def visit_even(self, spec: EvenSpecification) -> None:
        pass

    @abstractmethod
    def visit_greater_than(self, spec: GreaterThanSpecification) -> None:
        pass

    @abstractmethod
    def visit_and(self, spec: AndSpecification) -> None:
        pass

    @abstractmethod
    def visit_or(self, spec: OrSpecification) -> None:
        pass

    @abstractmethod
    def visit_not(self, spec: NotSpecification) -> None:
        pass


"""
Architectural Trade-off Analysis: Traversal Control and Information Exposure

1. Who is responsible for traversal?
   - Traversing in Visitee (Composite): Directory-style traversal works when execution order
     is strictly hierarchical and uniform. However, for grammar translation (DSL, AST, Infix expressions),
     the visitor must control when and how child nodes are visited to place brackets and binary operators.
   - Traversing in Visitor (Adopted here): Grants full flexibility for in-order, pre-order, or selective
     traversals required by compilers and human-readable translators. The trade-off is slight logic
     duplication if multiple visitors must traverse the tree identically.

2. Breaking Encapsulation vs Exposure:
   - Visitors require structural details (left, right, operand, threshold) to do their job.
   - Domain classes expose read-only properties to prevent exposing internal mutable state directly,
     minimizing the architectural cost of breaking encapsulation.
"""


# Visitor
class PersianRuleTranslatorVisitor(SpecificationVisitorInterface):
    """
    Concrete Visitor that translates a composite specification tree into human-readable Persian text.
    Maintains an accumulated string buffer representing the in-order expression traversal.
    """

    def __init__(self) -> None:
        self._tokens: List[str] = []

    def get_text(self) -> str:
        return "".join(self._tokens)

    def visit_positive(self, spec: PositiveSpecification) -> None:
        self._tokens.append("مثبت باشد")

    def visit_even(self, spec: EvenSpecification) -> None:
        self._tokens.append("زوج باشد")

    def visit_greater_than(self, spec: GreaterThanSpecification) -> None:
        self._tokens.append(f"بزرگ‌تر از {spec.threshold} باشد")

    def visit_and(self, spec: AndSpecification) -> None:
        self._tokens.append("(")
        spec.left.accept(self)
        self._tokens.append(" و ")
        spec.right.accept(self)
        self._tokens.append(")")

    def visit_or(self, spec: OrSpecification) -> None:
        self._tokens.append("(")
        spec.left.accept(self)
        self._tokens.append(" یا ")
        spec.right.accept(self)
        self._tokens.append(")")

    def visit_not(self, spec: NotSpecification) -> None:
        self._tokens.append("نقیض (")
        spec.operand.accept(self)
        self._tokens.append(")")


if __name__ == "__main__":
    rule = PositiveSpecification().and_(
        EvenSpecification().or_(GreaterThanSpecification(10))
    )

    translator = PersianRuleTranslatorVisitor()
    rule.accept(translator)
    print("Persian Translation:")
    print(translator.get_text())

    test_value = 12
    is_valid = rule.is_satisfied_by(test_value)
    print(f"\nValue {test_value} satisfies rule: {is_valid}")
