
class Burger:
    
    def __init__(self, builder):
        self._size = builder.size
        self._cheese = builder.cheese
        self._pepperoni = builder.pepperoni
        self._lettuce = builder.lettuce
        self._tomato = builder.tomato
    
    def __str__(self):
        return f'A size={self._size} burger with: cheeze: {self._cheese}, pepperoni: {self._pepperoni}, lettuce: {self._lettuce}, tomato: {self._tomato}'


class BurgerBuilder:
    
    def __init__(self, size):
        self.size = size
        self.pepperoni = False
        self.lettuce = False
        self.cheese = False
        self.tomato = False
    
    def add_pepperoni(self):
        self.pepperoni = True
        return self
    
    def add_lettuce(self):
        self.lettuce = True
        return self
    
    def add_cheese(self):
        self.cheese = True
        return self
    
    def add_tomato(self):
        self.tomato = True
        return self
    
    def build(self):
        return Burger(builder=self)


burger = BurgerBuilder(size=14).add_cheese().add_pepperoni().build()
print(burger)

burger = BurgerBuilder(size=18).add_tomato().add_lettuce().add_pepperoni().build()
print(burger)
