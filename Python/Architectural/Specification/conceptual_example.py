from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass


class AbstractSpecification(ABC):
    """
    Abstract Specification defining the interface and providing template methods
    for composite logical operations (__and__, __or__, __invert__).
    Concrete subclasses must implement the is_satisfied_by method.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        pass

    def __and__(self, other: "AbstractSpecification") -> "AndSpecification":
        return AndSpecification(left_specification=self, right_specification=other)

    def __or__(self, other: "AbstractSpecification") -> "OrSpecification":
        return OrSpecification(left_specification=self, right_specification=other)

    def __invert__(self) -> "NotSpecification":
        return NotSpecification(wrapped_specification=self)


class AndSpecification(AbstractSpecification):
    """
    Composite specification representing logical AND.
    """

    def __init__(
        self,
        left_specification: AbstractSpecification,
        right_specification: AbstractSpecification,
    ) -> None:
        self.left_specification = left_specification
        self.right_specification = right_specification

    def is_satisfied_by(self, candidate: Any) -> bool:
        return (
            self.left_specification.is_satisfied_by(candidate)
            and self.right_specification.is_satisfied_by(candidate)
        )


class OrSpecification(AbstractSpecification):
    """
    Composite specification representing logical OR.
    """

    def __init__(
        self,
        left_specification: AbstractSpecification,
        right_specification: AbstractSpecification,
    ) -> None:
        self.left_specification = left_specification
        self.right_specification = right_specification

    def is_satisfied_by(self, candidate: Any) -> bool:
        return (
            self.left_specification.is_satisfied_by(candidate)
            or self.right_specification.is_satisfied_by(candidate)
        )


class NotSpecification(AbstractSpecification):
    """
    Composite specification representing logical NOT.
    """

    def __init__(self, wrapped_specification: AbstractSpecification) -> None:
        self.wrapped_specification = wrapped_specification

    def is_satisfied_by(self, candidate: Any) -> bool:
        return not self.wrapped_specification.is_satisfied_by(candidate)


# Concrete domain model and business specifications

@dataclass
class Product:
    name: str
    price: float
    stock_quantity: int
    is_active: bool


class InStockSpecification(AbstractSpecification):
    def is_satisfied_by(self, candidate: Product) -> bool:
        return candidate.stock_quantity > 0


class ActiveProductSpecification(AbstractSpecification):
    def is_satisfied_by(self, candidate: Product) -> bool:
        return candidate.is_active


class PremiumPriceSpecification(AbstractSpecification):
    def __init__(self, minimum_price: float) -> None:
        self.minimum_price = minimum_price

    def is_satisfied_by(self, candidate: Product) -> bool:
        return candidate.price >= self.minimum_price


if __name__ == "__main__":
    laptop = Product(name="Laptop", price=1200.0, stock_quantity=5, is_active=True)
    out_of_stock_accessory = Product(
        name="Cable", price=20.0, stock_quantity=0, is_active=True
    )
    inactive_item = Product(
        name="Old Item", price=1500.0, stock_quantity=10, is_active=False
    )

    is_in_stock = InStockSpecification()
    is_active = ActiveProductSpecification()
    is_premium = PremiumPriceSpecification(minimum_price=1000.0)

    # Complex rule: Active AND ((Premium AND InStock) OR (~Premium AND ~InStock))
    eligible_for_special_campaign = is_active & (
        (is_premium & is_in_stock) | (~is_premium & ~is_in_stock)
    )

    print(
        f"Is {laptop.name} eligible: "
        f"{eligible_for_special_campaign.is_satisfied_by(laptop)}"
    )
    print(
        f"Is {out_of_stock_accessory.name} eligible: "
        f"{eligible_for_special_campaign.is_satisfied_by(out_of_stock_accessory)}"
    )
    print(
        f"Is {inactive_item.name} eligible: "
        f"{eligible_for_special_campaign.is_satisfied_by(inactive_item)}"
    )
