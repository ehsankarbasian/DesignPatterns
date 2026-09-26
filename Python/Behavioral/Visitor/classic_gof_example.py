"""
Classic GoF Equipment example demonstrating the Visitor pattern combined with Composite.

Purpose & Context:
Demonstrates how the Visitor pattern scales when dealing with a rich, heterogeneous
domain model containing multiple distinct Leaf types (FloppyDisk, Card) and multiple
Composite types (Bus, Chassis).

Unlike simpler single-leaf examples, this canonical implementation from the GoF book
illustrates:
1. Interface Growth: As concrete element types grow, the visitor interface expands
   with dedicated visit methods (visit_floppy_disk, visit_card, visit_chassis, etc.).
2. High Cohesion & Decoupling: Complex, multi-faceted business operations (such as
   calculating net and discount pricing, or assembling an inventory bill-of-materials)
   evolve independently without polluting the equipment domain classes.
3. The Classical Trade-off: Adding new operations is trivial (Open-Closed Principle),
   while adding new equipment types requires updating all visitor classes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# Pattern Role: Component / Visitee Interface
class Equipment(ABC):

    def __init__(self, name: str, power: float, net_price: float, discount_price: float) -> None:
        self.name = name
        self.power = power
        self.net_price = net_price
        self.discount_price = discount_price

    # First Dispatch: dynamically dispatches based on the concrete equipment instance
    @abstractmethod
    def accept(self, visitor: EquipmentVisitor) -> None:
        pass


# Pattern Role: Leaf / Concrete Visitee (Storage Device)
class FloppyDisk(Equipment):

    # Second Dispatch: binds self to visit_floppy_disk
    def accept(self, visitor: EquipmentVisitor) -> None:
        visitor.visit_floppy_disk(self)


# Pattern Role: Leaf / Concrete Visitee (Expansion Card)
class Card(Equipment):

    # Second Dispatch: binds self to visit_card
    def accept(self, visitor: EquipmentVisitor) -> None:
        visitor.visit_card(self)


# Pattern Role: Base Composite / Composite Equipment Abstraction
class CompositeEquipment(Equipment):

    def __init__(self, name: str, power: float = 0.0, net_price: float = 0.0, discount_price: float = 0.0) -> None:
        super().__init__(name, power, net_price, discount_price)
        self._parts: list[Equipment] = []

    def add(self, equipment: Equipment) -> None:
        self._parts.append(equipment)

    def remove(self, equipment: Equipment) -> None:
        self._parts.remove(equipment)

    @property
    def parts(self) -> list[Equipment]:
        return self._parts


# Pattern Role: Composite / Concrete Visitee (Hardware Communication Bus)
class Bus(CompositeEquipment):

    # Traverses self, then propagates accept down to connected cards/controllers
    def accept(self, visitor: EquipmentVisitor) -> None:
        visitor.visit_bus(self)
        for part in self._parts:
            part.accept(visitor)


# Pattern Role: Composite / Concrete Visitee (Computer Chassis / Outer Casing)
class Chassis(CompositeEquipment):

    # Traverses self, then propagates accept down to internal components and buses
    def accept(self, visitor: EquipmentVisitor) -> None:
        visitor.visit_chassis(self)
        for part in self._parts:
            part.accept(visitor)


# Pattern Role: Visitor Interface
# Note how the interface scales with each new concrete equipment leaf and composite
class EquipmentVisitor(ABC):

    @abstractmethod
    def visit_floppy_disk(self, floppy: FloppyDisk) -> None:
        pass

    @abstractmethod
    def visit_card(self, card: Card) -> None:
        pass

    @abstractmethod
    def visit_bus(self, bus: Bus) -> None:
        pass

    @abstractmethod
    def visit_chassis(self, chassis: Chassis) -> None:
        pass


# Pattern Role: Concrete Visitor (Financial & Pricing Calculation Operation)
class PricingVisitor(EquipmentVisitor):

    def __init__(self) -> None:
        self.total_net_price: float = 0.0
        self.total_discount_price: float = 0.0

    def visit_floppy_disk(self, floppy: FloppyDisk) -> None:
        self.total_net_price += floppy.net_price
        self.total_discount_price += floppy.discount_price

    def visit_card(self, card: Card) -> None:
        self.total_net_price += card.net_price
        self.total_discount_price += card.discount_price

    def visit_bus(self, bus: Bus) -> None:
        self.total_net_price += bus.net_price
        self.total_discount_price += bus.discount_price

    def visit_chassis(self, chassis: Chassis) -> None:
        self.total_net_price += chassis.net_price
        self.total_discount_price += chassis.discount_price


# Pattern Role: Concrete Visitor (Inventory & Bill-of-Materials Reporting)
class InventoryVisitor(EquipmentVisitor):

    def __init__(self) -> None:
        self.inventory: list[str] = []
        self.total_power: float = 0.0

    def visit_floppy_disk(self, floppy: FloppyDisk) -> None:
        self.inventory.append(f"Floppy Disk: {floppy.name}")
        self.total_power += floppy.power

    def visit_card(self, card: Card) -> None:
        self.inventory.append(f"Expansion Card: {card.name}")
        self.total_power += card.power

    def visit_bus(self, bus: Bus) -> None:
        self.inventory.append(f"System Bus: {bus.name}")
        self.total_power += bus.power

    def visit_chassis(self, chassis: Chassis) -> None:
        self.inventory.append(f"Chassis Enclosure: {chassis.name}")
        self.total_power += chassis.power


"""
Architectural Trade-off Analysis of the Visitor Pattern:

1. What is EASY (Adding New Operations):
   - Introducing an entirely new cross-cutting behavior—such as a WarrantyVisitor,
     TaxCalculationVisitor, or PowerConsumptionReportVisitor—is trivial.
   - We define a new class implementing EquipmentVisitor without touching,
     recompiling, or risking regressions in any existing Equipment classes.
   - The Open/Closed Principle (OCP) is strictly upheld for operations.

2. What is HARD (Adding New Elements / Types):
   - Introducing a new hardware type—such as a PowerSupply, Motherboard, or GPU—is costly.
   - Step 1: EquipmentVisitor must declare a new abstract method: `visit_power_supply(...)`.
   - Step 2: Every existing Concrete Visitor (PricingVisitor, InventoryVisitor, etc.)
     breaks immediately until it implements that new method.
   - The Open/Closed Principle is VIOLATED when the object structure is volatile.

Design Guideline:
Use the Visitor pattern when the element class hierarchy is STABLE, but the operations
performed over those elements change frequently or are open-ended.
"""

# Pattern Role: Client Code
if __name__ == "__main__":

    # Construct the multi-level computer assembly
    pc_chassis = Chassis("PC Case Tower", power=15.0, net_price=80.0, discount_price=70.0)
    system_bus = Bus("PCIe System Bus", power=5.0, net_price=40.0, discount_price=35.0)

    # Attach components to composite nodes
    pc_chassis.add(system_bus)
    pc_chassis.add(FloppyDisk("3.5-inch Floppy Drive", power=8.0, net_price=25.0, discount_price=20.0))

    system_bus.add(Card("16-bit Sound Card", power=12.0, net_price=65.0, discount_price=55.0))
    system_bus.add(Card("Network Interface Card", power=10.0, net_price=45.0, discount_price=40.0))

    # Operation 1: Calculate total pricing across the assembly
    pricing_visitor = PricingVisitor()
    pc_chassis.accept(pricing_visitor)

    print("Equipment Pricing Summary:")
    print(f"Total Net Price: ${pricing_visitor.total_net_price:.2f}")
    print(f"Total Discount Price: ${pricing_visitor.total_discount_price:.2f}")

    # Operation 2: Assemble inventory list and compute total power draw
    inventory_visitor = InventoryVisitor()
    pc_chassis.accept(inventory_visitor)

    print("\nInventory Bill-of-Materials:")
    for item in inventory_visitor.inventory:
        print(f" - {item}")
    print(f"Total Power Consumption: {inventory_visitor.total_power} Watts")
