from abc import ABC, abstractmethod


# AbstractFactory
class CoffeeFactory(ABC):

    @abstractmethod
    def create_coffee_without_milk(self):
        pass

    @abstractmethod
    def create_coffee_with_milk(self):
        pass


# ConcreteFactory
class ItalianCoffeeFactory(CoffeeFactory):

    def create_coffee_without_milk(self):
        return ItalianEspresso()

    def create_coffee_with_milk(self):
        return ItalianCappucino()


class FrenchCoffeeFactory(CoffeeFactory):

    def create_coffee_without_milk(self):
        return FrenchEspresso()

    def create_coffee_with_milk(self):
        return FrenchCappucino()


# AbstractProducts
class CoffeeWithOutMilk(ABC):

    @abstractmethod
    def prepare(self, CoffeeWithOutMilk):
        pass


class CoffeeWithMilk(ABC):

    @abstractmethod
    def serve(self, CoffeeWithOutMilk):
        pass


# ConcreteProducts
class ItalianEspresso(CoffeeWithOutMilk):

    def prepare(self):
        print("\nPrepare:", type(self).__name__)


class ItalianCappucino(CoffeeWithMilk):

    def serve(self):
        print(type(self).__name__, "is served with sheep's milk")


class FrenchEspresso(CoffeeWithOutMilk):

    def prepare(self):
        print("\nPrepare:", type(self).__name__)


class FrenchCappucino(CoffeeWithMilk):

    def serve(self):
        print(type(self).__name__, "is served with cow's milk")


italian_factory = ItalianCoffeeFactory()
without_milk = italian_factory.create_coffee_without_milk()
without_milk.prepare()
with_milk = italian_factory.create_coffee_with_milk()
with_milk.serve()

franch_factory = FrenchCoffeeFactory()
without_milk = franch_factory.create_coffee_without_milk()
without_milk.prepare()
with_milk = franch_factory.create_coffee_with_milk()
with_milk.serve()
