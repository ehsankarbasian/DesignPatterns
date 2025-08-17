from abc import ABC, abstractmethod


class WritingState(ABC):
    
    @abstractmethod
    def write(self, word):
        pass


class DefaultText(WritingState):
    
    def write(self, word):
        print(word)


class UpperCase(WritingState):
    
    def write(self, word):
        print(word.upper())


class LowerCase(WritingState):
    
    def write(self, word):
        print(word.lower())


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


editor = TextEditor(DefaultText())
editor.type_text('First line')

editor.state = UpperCase()
editor.type_text('Second line')
editor.type_text('Third line')

editor.state = LowerCase()
editor.type_text('Forth line')
editor.type_text('Fifth line')
