from abc import ABC, abstractmethod


class CoffeeInterface(ABC):
    
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass


class SimpleCoffee(CoffeeInterface):
    
    def get_cost(self):
        return 10
    
    def get_description(self):
        return 'Simple coffee'


class MilkCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    def get_cost(self):
        return self._coffee.get_cost() + 2
    
    def get_description(self):
        return self._coffee.get_description() + ", milk"


class WhipCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    def get_cost(self):
        return self._coffee.get_cost() + 5
    
    def get_description(self):
        return self._coffee.get_description() + ", whip"


class VanillaCoffee(CoffeeInterface):
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    def get_cost(self):
        return self._coffee.get_cost() + 3
    
    def get_description(self):
        return self._coffee.get_description() + ", vanilla"


some_coffee = SimpleCoffee()
print(some_coffee.get_cost())
print(some_coffee.get_description(), '\n')

some_coffee = MilkCoffee(some_coffee)
print(some_coffee.get_cost())
print(some_coffee.get_description(), '\n')

some_coffee = WhipCoffee(some_coffee)
print(some_coffee.get_cost())
print(some_coffee.get_description(), '\n')

some_coffee = VanillaCoffee(some_coffee)
print(some_coffee.get_cost())
print(some_coffee.get_description())
