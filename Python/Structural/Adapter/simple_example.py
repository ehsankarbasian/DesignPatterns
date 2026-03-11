from abc import ABC, abstractmethod


class LionInterface(ABC):
    @abstractmethod
    def roar(self):
        pass


class AfricanLion(LionInterface):
    def roar(self):
        print("BLACK ROAR !!!")


class AsianLion(LionInterface):
    def roar(self):
        print("BROWN ROAR !!!")


class Hunter:
    def hunt(self, animal):
        animal.roar()
        print("I am 2 meters tall, I have 10 pistols. POWAAGHHH...", '\n')


class Donkey:
    def ar_ar(self):
        print("AR AR !!!")


hunter = Hunter()
lion_1 = AfricanLion()
lion_2 = AsianLion()
hunter.hunt(lion_1)
hunter.hunt(lion_2)

# donkey = Donkey()
# hunter.hunt(donkey)
# Can't hunt the donkey because donkey doesn't roar()
# Must adapt the behaviour to be huntable by lion hunter


class DonkeyAdapter(LionInterface):
    
    def __init__(self, donkey):
        self._donkey = donkey
    
    def roar(self):
        self._donkey.ar_ar()


donkey = Donkey()
adapted_donkey = DonkeyAdapter(donkey)
hunter.hunt(adapted_donkey)


# Can be implemented like this too:
# Benefit: No need to use or even import the Donkey class in the client code

class DonkeyAdapter(LionInterface, Donkey):
    
    def roar(self):
        print('Inside adapted', end=' ')
        self.ar_ar()

adapted_donkey = DonkeyAdapter()
hunter.hunt(adapted_donkey)
