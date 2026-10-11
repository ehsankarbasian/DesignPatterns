"""
Hierarchical storage placement via greedy chain on composite tree.

Comparison with composite_branch_router.py:
    Unlike composite_branch_router.py, which separates bounded contexts (HR, Finance,
    Legal) allowing isolated multi-team ownership and mapping cleanly to message buses,
    this file models a uniform physical resource allocation domain. Containers share
    an identical domain contract where responsibility delegation is implicit through
    composite call-stack iteration rather than explicit successor references.

Trade-offs:
    First-fit allocation favors earlier containers causing branch fragmentation.
    Visitor separates graph visualization from domain mutation rules.
"""

from abc import ABC, abstractmethod
from typing import List


# Payload volume holder enforcing domain invariants
# Domain entity
class Item:
    """
    Volume carrier entity validated against non-positive allocation size.
    """

    def __init__(self, size: int) -> None:
        self.size = size

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Item size must be a positive integer")
        self._size = value


# Inspection protocol across storage structure
# Visitor interface
class StorageVisitorInterface(ABC):
    """
    Inspection contract traversing hierarchical storage elements.
    """

    @abstractmethod
    def visit_box(self, box: "Box") -> None:
        pass

    @abstractmethod
    def visit_shelf(self, shelf: "Shelf") -> None:
        pass


# Storage component contract handling capacity evaluation and item placement
# Component, Handler
class ContainerInterface(ABC):
    """
    Component contract combining composite hierarchy and handling responsibility.
    """

    @property
    @abstractmethod
    def total_capacity(self) -> int:
        pass

    @property
    @abstractmethod
    def remaining_capacity(self) -> int:
        pass

    @abstractmethod
    def can_put_item(self, item: Item) -> bool:
        pass

    @abstractmethod
    def put_item(self, item: Item) -> bool:
        pass

    @abstractmethod
    def accept(self, visitor: StorageVisitorInterface) -> None:
        pass


# Leaf container storing items against internal capacity limit
# Leaf, Terminal Handler
class Box(ContainerInterface):
    """
    Terminal storage container holding discrete items and managing local bounds.

    Trade-offs:
        Mutating internal state directly avoids allocation stack overhead.
        Fixed bounds reject fragmented items exceeding remaining volume.
    """

    def __init__(self, capacity: int, name: str = "Box") -> None:
        if capacity <= 0:
            raise ValueError("Container capacity must be positive")
        self.name = name
        self._capacity = capacity
        self._items: List[Item] = []

    @property
    def total_capacity(self) -> int:
        return self._capacity

    @property
    def remaining_capacity(self) -> int:
        used = sum(item.size for item in self._items)
        return self._capacity - used

    def can_put_item(self, item: Item) -> bool:
        return self.remaining_capacity >= item.size

    def put_item(self, item: Item) -> bool:
        if self.can_put_item(item):
            self._items.append(item)
            return True
        return False

    def accept(self, visitor: StorageVisitorInterface) -> None:
        visitor.visit_box(self)


# Composite container distributing item placement across nested containers
# Composite, Distributed Branch Handler
class Shelf(ContainerInterface):
    """
    Branch storage container dispatching placement down child branches.

    Trade-offs:
        Recursive delegation simplifies client interaction at tree root.
        Greedy candidate search produces uneven child node utilization.
    """

    def __init__(self, name: str = "Shelf") -> None:
        self.name = name
        self._inner_containers: List[ContainerInterface] = []

    def add_container(self, *containers: ContainerInterface) -> None:
        self._inner_containers.extend(containers)

    @property
    def inner_containers(self) -> List[ContainerInterface]:
        return list(self._inner_containers)

    @property
    def total_capacity(self) -> int:
        return sum(c.total_capacity for c in self._inner_containers)

    @property
    def remaining_capacity(self) -> int:
        return sum(c.remaining_capacity for c in self._inner_containers)

    def can_put_item(self, item: Item) -> bool:
        return any(c.can_put_item(item) for c in self._inner_containers)

    def put_item(self, item: Item) -> bool:
        for candidate in self._inner_containers:
            if candidate.can_put_item(item):
                return candidate.put_item(item)
        return False

    def accept(self, visitor: StorageVisitorInterface) -> None:
        visitor.visit_shelf(self)
        for child in self._inner_containers:
            child.accept(visitor)


# Tree traversal printer accumulating formatted capacity state
# Concrete Visitor
class GraphDrawerVisitor(StorageVisitorInterface):
    """
    Concrete visitor formatting capacity metrics into displayable hierarchy.

    Trade-offs:
        Externalizes presentation state without polluting domain models.
        Requires dual dispatch hooks across every concrete container type.
    """

    def __init__(self) -> None:
        self._lines: List[str] = []
        self._depth = 0

    def visit_shelf(self, shelf: Shelf) -> None:
        indent = "  " * self._depth
        line = (
            f"{indent}{shelf.name} (Cap: {shelf.total_capacity} | "
            f"Remaining: {shelf.remaining_capacity})"
        )
        self._lines.append(line)

    def visit_box(self, box: Box) -> None:
        indent = "  " * (self._depth + 1)
        line = (
            f"{indent}{box.name} (Cap: {box.total_capacity} | "
            f"Remaining: {box.remaining_capacity})"
        )
        self._lines.append(line)

    def get_graph(self) -> str:
        return "\n".join(self._lines)


def draw_graph(root: ContainerInterface) -> str:
    visitor = GraphDrawerVisitor()
    root.accept(visitor)
    return visitor.get_graph()


if __name__ == "__main__":
    shelf1 = Shelf(name="RootShelf")
    shelf2 = Shelf(name="Shelf2")
    shelf3 = Shelf(name="Shelf3")

    shelf1.add_container(shelf2, shelf3)

    box1 = Box(capacity=10, name="Box1")
    box2 = Box(capacity=20, name="Box2")
    box3 = Box(capacity=15, name="Box3")
    box4 = Box(capacity=30, name="Box4")

    shelf2.add_container(box1, box2)
    shelf3.add_container(box3, box4)

    item1 = Item(size=28)
    shelf1.put_item(item1)

    item2 = Item(size=15)
    shelf1.put_item(item2)

    print(draw_graph(shelf1))
