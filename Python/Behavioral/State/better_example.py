from abc import ABC, abstractmethod


"""
State can be considered as an extension of Strategy.
Both patterns are based on composition:
    they change the behavior of the context by delegating some work to helper objects.

Strategy makes these objects completely independent and unaware of each other.

State doesn't restrict dependencies between concrete states,
letting them alter the state of the context at will.

READ MORE: https://refactoring.guru/design-patterns/state
"""


class WritingState(ABC):
    
    @abstractmethod
    def write(self, word):
        pass
    
    @abstractmethod
    def get_new_state_instance(self):
        pass
    
    def switch_state(self, text_editor):
        text_editor.state = self.get_new_state_instance()


class DefaultText(WritingState):
    
    def write(self, word):
        print(word)
    
    def get_new_state_instance(self):
        return UpperCase()


class UpperCase(WritingState):
    
    def write(self, word):
        print(word.upper())
    
    def get_new_state_instance(self):
        return LowerCase()


class LowerCase(WritingState):
    
    def write(self, word):
        print(word.lower())
    
    def get_new_state_instance(self):
        return DefaultText()


class TextEditor:
    
    def __init__(self, state):
        self._state = state
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
    
    def type_text(self, text):
        self.state.write(text)
    
    def switch_text_format(self):
        self.state.switch_state(text_editor=self)


editor = TextEditor(DefaultText())
editor.type_text('First Line')
editor.switch_text_format()
editor.type_text('Second Line')
editor.switch_text_format()
editor.type_text('Third Line')
editor.switch_text_format()
editor.type_text('Forth Line')

print()
editor.state = UpperCase()
editor.type_text('Fifth Line')
editor.switch_text_format()
editor.type_text('Sixth Line')
editor.switch_text_format()
editor.type_text('Seventh Line')
editor.switch_text_format()
editor.type_text('Eighth Line')

print()
editor.state = LowerCase()
editor.type_text('Nineth Line')
editor.switch_text_format()
editor.type_text('Tenth Line')
editor.switch_text_format()
editor.type_text('Eleventh Line')
editor.switch_text_format()
editor.type_text('Twelveth Line')
