from __future__ import annotations
from abc import ABC, abstractmethod


# Visitee
class AnimalInterface(ABC):
    
    @abstractmethod
    def accept(self, operation: AnimalOperationInterface):
        pass


# Visitor
class AnimalOperationInterface(ABC):
    
    @abstractmethod
    def visit_monkey(self, monkey: Monkey):
        pass
    
    @abstractmethod
    def visit_lion(self, lion: Lion):
        pass
    
    @abstractmethod
    def visit_dolphin(self, dolphin: Dolphin):
        pass


# Concrete Visitee
class Monkey(AnimalInterface):
    
    def shout(self):
        print('O oo o AA AA aa !')
    
    def accept(self, operation):
        operation.visit_monkey(monkey=self)


class Lion(AnimalInterface):
    
    def roar(self):
        print('Roaaar !')
    
    def accept(self, operation):
        operation.visit_lion(lion=self)


class Dolphin(AnimalInterface):
    
    def speak(self):
        print('Tuut tu tuuuu tuutt!')
    
    def accept(self, operation):
        operation.visit_dolphin(dolphin=self)


# Concrete Visitor
class Speak(AnimalOperationInterface):
    
    def visit_monkey(self, monkey):
        monkey.shout()
    
    def visit_lion(self, lion):
        lion.roar()
    
    def visit_dolphin(self, dolphin):
        dolphin.speak()


class Jump(AnimalOperationInterface):
    
    def visit_monkey(self, monkey):
        print('Jumped 20 feet high! on to the tree!')
    
    def visit_lion(self, lion):
        print('Jumped 7 feet! Back on the ground!')
    
    def visit_dolphin(self, dolphin):
        print('Walked on water a little and disappeared')


if __name__ == "__main__":
    monkey = Monkey()
    lion = Lion()
    dolphin = Dolphin()
    
    speak = Speak()
    monkey.accept(speak)
    lion.accept(speak)
    dolphin.accept(speak)
    
    jump = Jump()
    monkey.accept(jump)
    lion.accept(jump)
    dolphin.accept(jump)
