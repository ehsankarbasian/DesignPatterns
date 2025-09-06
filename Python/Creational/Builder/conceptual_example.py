from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


# Code from: "https://refactoring.guru/design-patterns/builder/python/example"

class AbstractBuilder(ABC):

    @property
    @abstractmethod
    def product(self):
        pass

    @abstractmethod
    def produce_part_a(self):
        pass

    @abstractmethod
    def produce_part_b(self):
        pass

    @abstractmethod
    def produce_part_c(self):
        pass


class ConcreteBuilder(AbstractBuilder):

    def __init__(self):
        self.reset()

    def reset(self):
        self._product = Product()

    @property
    def product(self) -> Product:
        product = self._product
        self.reset()
        return product

    def produce_part_a(self):
        self._product.add("PartA1")

    def produce_part_b(self):
        self._product.add("PartB1")

    def produce_part_c(self):
        self._product.add("PartC1")


class Product:
    
    def __init__(self):
        self.parts = []

    def add(self, part: Any):
        self.parts.append(part)

    @property
    def list_parts(self) -> str:
        return f"Product parts: {', '.join(self.parts)}\n"


class Director:

    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> AbstractBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: AbstractBuilder):
        self._builder = builder

    def build_minimal_viable_product(self):
        self.builder.produce_part_a()

    def build_full_featured_product(self):
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()


if __name__ == "__main__":
    
    director = Director()
    builder = ConcreteBuilder()
    director.builder = builder

    print("Standard basic product: ")
    director.build_minimal_viable_product()
    print(builder.product.list_parts) #PartA1

    print("Standard full featured product: ")
    director.build_full_featured_product()
    print(builder.product.list_parts) #PartA1, PartB1, PartC1

    # Remember, the Builder pattern can be used without a Director class.
    print("Custom product: ")
    builder.produce_part_a()
    builder.produce_part_b()
    print(builder.product.list_parts) #PartA1, PartB1
