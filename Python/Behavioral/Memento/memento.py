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
    
    def type_(self, words: str):
        self._content += ' ' + words
    
    @property
    def content(self) -> str:
        return self._content
    
    def save(self) -> EditorMemento:
        return EditorMemento(self.content)
    
    def restore(self, memento: EditorMemento) -> None:
        self._content = memento.content


if __name__ == "__main__":
    editor = Editor()
    
    editor.type_('This is the first sentence.')
    editor.type_('This is second.')
    saved = editor.save()
    
    editor.type_('And this is third.')
    print(editor.content)
    
    editor.restore(saved)
    print(editor.content)
