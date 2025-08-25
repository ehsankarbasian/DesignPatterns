from abc import ABC, abstractmethod


# AbstractProduct_1
class Door(ABC):
    
    @abstractmethod
    def get_description(self):
        pass


# ConcreteProduct_1
class WoodenDoor(Door):
    
    def get_description(self):
        print('\nI am a wooden door')


class IronDoor(Door):
    
    def get_description(self):
        print('\nI am an iron door')


# AbstractProduct_2
class DoorFittingExpert(ABC):
    
    @abstractmethod
    def get_description(self):
        pass


# ConcreteProduct_2
class Welder(DoorFittingExpert):
    
    def get_description(self):
        print('I can only fit iron doors')


class Carpenter(DoorFittingExpert):
    
    def get_description(self):
        print('I can only fit wooden doors')


# AbstractFactory
class DoorFactory(ABC):
    
    @abstractmethod
    def make_door(self):
        pass
    
    @abstractmethod
    def make_fitting_expert(self):
        pass


# ConcreteFactory
class WoodenDoorFactory(DoorFactory):
    
    def make_door(self):
        return WoodenDoor()
    
    def make_fitting_expert(self):
        return Carpenter()


class IronDoorFactory(DoorFactory):
    
    def make_door(self):
        return IronDoor()
    
    def make_fitting_expert(self):
        return Welder()


wooden_factory = WoodenDoorFactory()
door = wooden_factory.make_door()
expert = wooden_factory.make_fitting_expert()
door.get_description()
expert.get_description()

iron_factory = IronDoorFactory()
door = iron_factory.make_door()
expert = iron_factory.make_fitting_expert()
door.get_description()
expert.get_description()
