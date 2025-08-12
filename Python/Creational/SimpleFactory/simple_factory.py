from abc import ABC, abstractmethod


class AbstractDoor(ABC):
    
    @property
    @abstractmethod
    def width(self):
        pass
    
    @property
    @abstractmethod
    def height(self):
        pass


class WoodenDoor(AbstractDoor):
    
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height


class DoorFactory:
    
    @staticmethod
    def make_door(width, height):
        return WoodenDoor(width, height)


door = DoorFactory.make_door(100, 200)
print(f'Width:  {door.width}')
print(f'Height: {door.height}')


# Benefit of class DoorFactory:
# No need to repeat the class WoodenDoor every where to create a door
# Can change only DoorFactory instead of AbstractDoor implementor everywhere
