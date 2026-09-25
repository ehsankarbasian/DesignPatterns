"""
Simple standalone example of the Visitor pattern.

Unlike conceptual_example.py, there is no composite structure here and
no typed accept/visit signatures; it only demonstrates the accept/visit
DOUBLE DISPATCH mechanism in its minimal form.
"""

"""
What is Single Dispatch ?

In standard single-dispatch object-oriented languages (such as Python, C++, and C#),
the runtime determines which concrete implementation of a method to execute based
solely on the runtime type of a single object: the receiver (`self`).

When an operation is invoked via `receiver.method(arg)`:
- The dispatch mechanism inspects only the runtime class of `receiver`.
- The type of `arg` is treated as plain data and plays no role in selecting
  the method implementation at runtime.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class AnimalInterface(ABC):
    
    @abstractmethod
    def accept(self, operation: AnimalOperationInterface) -> None:
        pass


class AnimalOperationInterface(ABC):
    
    @abstractmethod
    def visit_monkey(self, monkey: Monkey) -> None:
        pass

    @abstractmethod
    def visit_lion(self, lion: Lion) -> None:
        pass

    @abstractmethod
    def visit_dolphin(self, dolphin: Dolphin) -> None:
        pass


class Monkey(AnimalInterface):
    
    def accept(self, operation: AnimalOperationInterface) -> None:
        # Second Dispatch:
        # The concrete animal class explicitly binds its own type (`self`)
        # by calling the dedicated `visit_monkey` method on `operation`.
        # At runtime, dynamic dispatch resolves which concrete operation
        # (Speak or Jump) will execute.
        operation.visit_monkey(monkey=self)


class Lion(AnimalInterface):
    
    def accept(self, operation: AnimalOperationInterface) -> None:
        # Second Dispatch:
        operation.visit_lion(lion=self)


class Dolphin(AnimalInterface):
    
    def accept(self, operation: AnimalOperationInterface) -> None:
        # Second Dispatch:
        operation.visit_dolphin(dolphin=self)


class Speak(AnimalOperationInterface):
    
    def visit_monkey(self, monkey: Monkey) -> None:
        print(f"Monkey {id(monkey)}: O oo o AA AA aa !")

    def visit_lion(self, lion: Lion) -> None:
        print(f"Lion {id(lion)}: Roaaar !")

    def visit_dolphin(self, dolphin: Dolphin) -> None:
        print(f"Dolphin {id(dolphin)}: Tuut tu tuuuu tuutt!")


class Jump(AnimalOperationInterface):
    
    def visit_monkey(self, monkey: Monkey) -> None:
        print("Monkey jumped 20 feet high! on to the tree!")

    def visit_lion(self, lion: Lion) -> None:
        print("Lion jumped 7 feet! Back on the ground!")

    def visit_dolphin(self, dolphin: Dolphin) -> None:
        print("Dolphin walked on water a little and disappeared")


if __name__ == "__main__":
    
    animals: list[AnimalInterface] = [Monkey(), Lion(), Dolphin()]

    speak = Speak()
    jump = Jump()

    print("The same hierarchy, different external operations:")
    for animal in animals:
        # First Dispatch:
        # Calling `animal.accept(...)` resolves dynamically at runtime based on
        # the concrete runtime type of `animal` (Monkey, Lion, or Dolphin).
        animal.accept(speak)

    print("\nOperations are added without touching the animal classes:")
    for animal in animals:
        # First Dispatch again with a different concrete operation:
        animal.accept(jump)
