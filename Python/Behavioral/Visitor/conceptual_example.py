from __future__ import annotations
from abc import ABC, abstractmethod


# code_from: https://refactoring.guru/design-patterns/visitor/python/example

# Visitee interface
class ComponentInterface(ABC):

    @abstractmethod
    def accept(self, visitor: VisitorInterface) -> None:
        pass


# Concrete Visitees
class ConcreteComponentA(ComponentInterface):

    def accept(self, visitor: VisitorInterface) -> None:
        visitor.visit_concrete_component_a(self)

    def exclusive_method_of_concrete_component_a(self) -> str:
        """
        Concrete Components may have special methods that don't exist in their base class or interface.
        The Visitor is still able to use these methods since it's aware of the component's concrete class.
        """

        return "A"


class ConcreteComponentB(ComponentInterface):
    """
    Same here: visitConcreteComponentB => ConcreteComponentB
    """

    def accept(self, visitor: VisitorInterface):
        visitor.visit_concrete_component_b(self)

    def special_method_of_concrete_component_b(self) -> str:
        return "B"


class VisitorInterface(ABC):
    """
    The Visitor Interface declares a set of visiting methods that correspond to component classes
    """

    @abstractmethod
    def visit_concrete_component_a(self, element: ConcreteComponentA) -> None:
        pass

    @abstractmethod
    def visit_concrete_component_b(self, element: ConcreteComponentB) -> None:
        pass


"""
Concrete Visitors implement several versions of the same algorithm, which can
work with all concrete component classes.
"""


class ConcreteVisitor1(VisitorInterface):
    def visit_concrete_component_a(self, element) -> None:
        print(f"{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor1")

    def visit_concrete_component_b(self, element) -> None:
        print(f"{element.special_method_of_concrete_component_b()} + ConcreteVisitor1")


class ConcreteVisitor2(VisitorInterface):
    def visit_concrete_component_a(self, element) -> None:
        print(f"{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor2")

    def visit_concrete_component_b(self, element) -> None:
        print(f"{element.special_method_of_concrete_component_b()} + ConcreteVisitor2")


def client_code(components: list[ComponentInterface], visitor: VisitorInterface) -> None:
    """
    The accept operation directs a call to the appropriate operation in the visitor object
    """

    for component in components:
        component.accept(visitor)


if __name__ == "__main__":
    components = [ConcreteComponentA(), ConcreteComponentB()]

    print("The client code works with all visitors via the base Visitor interface:")
    visitor1 = ConcreteVisitor1()
    client_code(components, visitor1)
    print()
    print("It allows the same client code to work with different types of visitors:")
    visitor2 = ConcreteVisitor2()
    client_code(components, visitor2)
