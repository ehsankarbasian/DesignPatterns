from abc import ABC, abstractmethod


# Reciever
class Bulb:
    
    def turn_on(self):
        print('Turn on the bulb')
    
    def turn_off(self):
        print('Darkness !')


class CommandInterface(ABC):
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
    
    @abstractmethod
    def redo(self):
        pass


# Concrete commands
class TurnOn(CommandInterface):
    
    def __init__(self, bulb):
        self._bulb = bulb
    
    def execute(self):
        self._bulb.turn_on()
    
    def undo(self):
        self._bulb.turn_off()
    
    def redo(self):
        self.execute()


class TurnOff(CommandInterface):
    
    def __init__(self, bulb):
        self._bulb = bulb
    
    def execute(self):
        self._bulb.turn_off()
    
    def undo(self):
        self._bulb.turn_on()
    
    def redo(self):
        self.execute()


# Invoker class
class RemoteControl:
    
    def submit(self, command):
        command.execute()


# Client
bulb = Bulb()

turn_on = TurnOn(bulb=bulb)
turn_off = TurnOff(bulb=bulb)

remote = RemoteControl()
remote.submit(turn_on)
remote.submit(turn_off)
