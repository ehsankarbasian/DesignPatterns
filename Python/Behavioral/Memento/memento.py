from __future__ import annotations


class EditorMemento:
    
    def __init__(self, content: str):
        self._content = content
    
    @property
    def content(self) -> str:
        return self._content


class Editor:
    
    def __init__(self):
        self._content: str = ''
        self._mementos: list[EditorMemento] = [EditorMemento(content='')]
        self._memento_index: int = -1
    
    def type_(self, words: str):
        self._content += words
        self._save()
    
    def _save(self) -> None:
        memento = EditorMemento(self.content)
        
        if self._memento_index == -1:
            self._mementos.append(memento)
        else:
            self._mementos = self._mementos[0:self._memento_index+1] + [memento]
            self._memento_index = -1
    
    @property
    def content(self) -> str:
        return self._content
    
    def roll_back(self) -> None:
        if self._memento_index-1 < -len(self._mementos):
            print("Empty History: Can't roll back")
            return
            
        self._memento_index -= 1
        memento = self._mementos[self._memento_index]
        self._content = memento.content
    
    def roll_forward(self) -> None:
        if self._memento_index+1 > -1:
            print("No Forward History: Can't roll forward")
            return
        
        self._memento_index += 1
        memento = self._mementos[self._memento_index]
        self._content = memento.content


if __name__ == "__main__":
    editor = Editor()
    
    editor.type_('This is the first sentence.')
    editor.type_('This is second.')
    editor.type_('And this is third.')
    print(editor.content)
    
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    
    editor.roll_forward()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.type_('The NEW sentence.')
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_forward()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
    editor.roll_back()
    print(editor.content)
