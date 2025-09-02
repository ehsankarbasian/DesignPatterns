import random
from abc import ABC, abstractmethod


# Helper function to know is user authenticated or not
def is_authenticated():
    return bool(random.randint(0, 1))


class DoorInterface(ABC):
    
    @abstractmethod
    def open_(self):
        pass
    
    @abstractmethod
    def close(self):
        pass


class LabDoor(DoorInterface):
    
    def open_(self):
        print('Opening the lab door')
    
    def close(self):
        print('Closing the lab door')


class SecuredDoor(DoorInterface):
    
    def __init__(self, door):
        self._door = door
    
    def open_(self):
        if is_authenticated():
            self._door.open_()
        else:
            print("You can't enter at all")
    
    def close(self):
        self._door.close()


door = SecuredDoor(LabDoor())
door.open_()
door.open_()
door.close()
door.open_()
door.close()
