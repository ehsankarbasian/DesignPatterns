from abc import ABC, abstractmethod


# Entity interface
class CharacterInterface(ABC):
    
    @abstractmethod
    def render(self, name: str):
        pass


# Concrete Entity
class SharedCharacter(CharacterInterface):
    
    def __init__(self, height, weight, hair_color):
        self._height = height
        self._weight = weight
        self._hair_color = hair_color
    
    def render(self, name):
        print(f'Rendering a character with {self._height} height, {self._weight} weight and {self._hair_color} hair color.')


# FlyWeight Factory
class CharacterFactory:
    
    _characters: dict = {}
    
    def get_shared_characters(self, height, weight, hair_color):
        key = f'{height}-{weight}-{hair_color}'
        
        if key not in self._characters:
            print(f'Creating character {key}')
            self._characters[key] = SharedCharacter(height, weight, hair_color)
        
        return self._characters[key]


# Uses characters
class CharacterClient:
    
    _name: str
    _shared_character: CharacterInterface
    
    def __init__(self, name: str, factory: CharacterFactory, height, weight, hair_color):
        self._name = name
        self._shared_character = factory.get_shared_characters(height, weight, hair_color)
    
    def render(self):
        self._shared_character.render(self._name)


if __name__ == "__main__":
    factory = CharacterFactory()
    
    print()
    player_1 = CharacterClient('Player 1', factory, 180, 75, 'blonde')
    player_1.render()
    
    print()
    player_2 = CharacterClient('Player 2', factory, 180, 75, 'blonde')
    player_2.render()
    
    print()
    player_3 = CharacterClient('Player 3', factory, 190, 80, 'red')
    player_3.render()
