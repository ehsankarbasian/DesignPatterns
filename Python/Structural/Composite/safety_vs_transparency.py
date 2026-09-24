"""
Composite Pattern: Transparency vs. Type Safety

This module demonstrates the trade-off in managing child components within a
tree structure according to the Gang of Four (GoF):

1. Transparency Approach:
   Child management methods (add, remove) are declared in AbstractComponent.
   The client treats Leaf and Composite uniformly without type inspections.
   In Leaf nodes, these operations are implemented as safe no-op methods.

2. Type Safety Approach:
   Child management methods are declared exclusively in SafeComposite.
   AbstractSafeComponent only declares operations common to all nodes.
   The client relies on type checks when adding or removing children.
"""

from abc import ABC, abstractmethod
from typing import List


# Transparency Approach
# Enforcing child management interface across all components (including leaves).

class AbstractComponent(ABC):
    """
    Base component defining uniform operations and child management methods.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def add(self, component: "AbstractComponent") -> None:
        pass

    @abstractmethod
    def remove(self, component: "AbstractComponent") -> None:
        pass


class Leaf(AbstractComponent):
    """
    End-node element that does not support children (operations are explicit no-ops).
    """

    def execute(self) -> str:
        return f"Leaf({self.name})"

    def add(self, component: "AbstractComponent") -> None:
        pass

    def remove(self, component: "AbstractComponent") -> None:
        pass


class Composite(AbstractComponent):
    """
    Container element maintaining child components via AbstractComponent interface.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: List[AbstractComponent] = []

    def add(self, component: AbstractComponent) -> None:
        self.children.append(component)

    def remove(self, component: AbstractComponent) -> None:
        self.children.remove(component)

    def execute(self) -> str:
        results = [child.execute() for child in self.children]
        return f"Composite({self.name}) -> [{', '.join(results)}]"


# Type Safety Approach
# Restricting child management only to the Composite class to prevent invalid calls.

class AbstractSafeComponent(ABC):
    """
    Base component declaring only shared domain operations.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def execute(self) -> str:
        pass


class SafeLeaf(AbstractSafeComponent):
    """
    End-node element exposing only valid operations.
    """

    def execute(self) -> str:
        return f"SafeLeaf({self.name})"


class SafeComposite(AbstractSafeComponent):
    """
    Container element declaring explicit child management methods.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: List[AbstractSafeComponent] = []

    def add(self, component: AbstractSafeComponent) -> None:
        self.children.append(component)

    def remove(self, component: AbstractSafeComponent) -> None:
        self.children.remove(component)

    def execute(self) -> str:
        results = [child.execute() for child in self.children]
        return f"SafeComposite({self.name}) -> [{', '.join(results)}]"


# Client Code

def client_code_transparency(component: AbstractComponent) -> None:
    """
    Transparency Client:
    The client operates uniformly on any component (Leaf or Composite).
    It calls add() directly without inspecting the concrete type.
    If called on a Leaf, the operation silently behaves as a no-op.
    """
    # Attempt to add a new child directly through the base interface
    component.add(Leaf("New Leaf"))

    # Execute and display the resulting component hierarchy/output
    print(f"Transparency output: {component.execute()}")


def client_code_safety(component: AbstractSafeComponent) -> None:
    """
    Type Safety Client:
    The base interface only exposes execute(). To add child nodes safely,
    the client must check if the component is actually a composite container.
    """
    # Explicit type check required to access child-management operations
    if isinstance(component, SafeComposite):
        component.add(SafeLeaf("New Leaf"))
        print(f"SafeComposite output: {component.execute()}")
    else:
        print(f"SafeLeaf output (no children allowed): {component.execute()}")


if __name__ == "__main__":
    # --- 1. Testing Transparency ---
    # In Transparency, both Root and Leaf accept add() with identical interface.
    transparent_root = Composite("Root")
    transparent_leaf = Leaf("Leaf A")
    transparent_root.add(transparent_leaf)

    client_code_transparency(transparent_root)
    client_code_transparency(transparent_leaf)

    # --- 2. Testing Type Safety ---
    # In Safety, only SafeComposite exposes add(); Leaf never accepts children.
    safe_root = SafeComposite("Root")
    safe_leaf = SafeLeaf("Leaf A")
    safe_root.add(safe_leaf)

    client_code_safety(safe_root)
    client_code_safety(safe_leaf)
