from abc import ABC, abstractmethod


class CoffeeInterface(ABC):
    
    @property
    @abstractmethod
    def cost(self):
        pass
    
    @property
    @abstractmethod
    def description(self):
        pass


class SimpleCoffee(CoffeeInterface):
    
    @property
    def cost(self):
        return 10
    
    @property
    def description(self):
        return 'Simple coffee'


class MilkCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    @property
    def cost(self):
        return self._coffee.cost + 2
    
    @property
    def description(self):
        return self._coffee.description + ", milk"


class WhipCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    @property
    def cost(self):
        return self._coffee.cost + 5
    
    @property
    def description(self):
        return self._coffee.description + ", whip"


class VanillaCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    @property
    def cost(self):
        return self._coffee.cost + 3
    
    @property
    def description(self):
        return self._coffee.description + ", vanilla"


some_coffee = SimpleCoffee()
print(some_coffee.cost)
print(some_coffee.description, '\n')

some_coffee = MilkCoffee(some_coffee)
print(some_coffee.cost)
print(some_coffee.description, '\n')

some_coffee = WhipCoffee(some_coffee)
print(some_coffee.cost)
print(some_coffee.description, '\n')

some_coffee = VanillaCoffee(some_coffee)
print(some_coffee.cost)
print(some_coffee.description)
