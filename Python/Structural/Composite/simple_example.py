# Idea: Dive into DesignPatterns (page:179)

from __future__ import annotations
from abc import ABC, abstractmethod


class ItemInterface(ABC):
    
    @abstractmethod
    def total_price(self) -> float:
        pass


class Product(ItemInterface):
    
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def total_price(self) -> float:
        return self.price


class Box(ItemInterface):
    
    def __init__(self, name: str, packaging_cost: float = 0.0) -> None:
        self.name = name
        self.packaging_cost = packaging_cost
        self.items: list[ItemInterface] = []

    def add(self, item: ItemInterface) -> None:
        self.items.append(item)

    # Calculate total_price recursively over the composition tree
    def total_price(self) -> float:
        return self.packaging_cost + sum(item.total_price() for item in self.items)


# Client Code:
book = Product("Book", 20)
phone = Product("Phone", 300)

small_box = Box("Small Box", packaging_cost=5)
small_box.add(phone)

main_box = Box("Main Box", packaging_cost=10)
main_box.add(book)
main_box.add(small_box)

print(main_box.total_price())
