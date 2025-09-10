from abc import ABC, abstractmethod


class CommandInterface(ABC):
    
    def __init__(self, app, editor):
        self._app = app
        self._editor = editor
    
    def save_backup(self):
        self._backup = self._editor.text
    
    def undo(self):
        self._editor.text = self._backup
    
    @abstractmethod
    def execute(self):
        pass


class CopyCommand(CommandInterface):
    
    def execute(self):
        self.save_backup()
        self._app.clipboard = self._editor.get_selection()
        self._editor.delete_selection()


class PasteCommand(CommandInterface):
    
    def execute(self):
        self.save_backup()
        self._editor.replace_selection(self._app.clipboard)
        return True


class UndoCommand(CommandInterface):
    
    def execute(self):
        self._app.undo()
        return False


class CommandHistory:
    
    def __init__(self):
        self._history = []
    
    def push(self, command):
        self._history.append(command)

    def pop(self, command):
        return self._history.pop(command)


class Editor:
    
    def __init__(self):
        self.text = ''
    
    def get_selection(self):
        print('Returning selected text ...')
    
    def delete_selection(self):
        print('Deleting selected text ...')
    
    def replace_selection(self):
        print("Insert the clipboard's contents at the current position")


class Application:
    
    def __init__(self):
        self.clipboard = ''
        self.history = CommandHistory()
    
    def execute_command(self, command):
        if command.execute():
            self.history.push(command)

    def undo(self):
        command = self.history.pop()
        if command != None:
            command.undo()


if __name__ == "__main__":
    app = Application()
    editor = Editor()
    command = CopyCommand(app, editor)
    
    app.execute_command(command)
