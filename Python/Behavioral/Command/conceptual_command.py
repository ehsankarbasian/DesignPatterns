from __future__ import annotations
from abc import ABC, abstractmethod


# Code from: https://refactoring.guru/design-patterns/command/python/example

class CommandInterface(ABC):

    @abstractmethod
    def execute(self):
        pass


class SimpleCommand(CommandInterface):

    def __init__(self, payload: str):
        self._payload = payload

    def execute(self):
        print(f"SimpleCommand: See, I can do simple things like printing"
              f"({self._payload})")


class ComplexCommand(CommandInterface):

    def __init__(self, receiver: Receiver, a: str, b: str):
        self._receiver = receiver
        self._a = a
        self._b = b

    def execute(self):
        print("ComplexCommand: Complex stuff should be done by a receiver object", end="")
        self._receiver.do_something(self._a)
        self._receiver.do_something_else(self._b)


class Receiver:
    """
    The Receiver classes contain some important business logic.
    """

    def do_something(self, a: str):
        print(f"\nReceiver: Working on ({a}.)", end="")

    def do_something_else(self, b: str):
        print(f"\nReceiver: Also working on ({b}.)", end="")


class Invoker:
    """
    The Invoker is associated with one or several commands.
    It sends a request to the command.
    """

    _on_start = None
    _on_finish = None

    def set_on_start(self, command: CommandInterface):
        self._on_start = command

    def set_on_finish(self, command: CommandInterface):
        self._on_finish = command

    def do_something_important(self):
        """
        The Invoker does not depend on concrete command or receiver classes. The
        Invoker passes a request to a receiver indirectly, by executing a
        command.
        """

        print("Invoker: Does anybody want something done before I begin?")
        if isinstance(self._on_start, CommandInterface):
            self._on_start.execute()

        print("Invoker: ...doing something really important...")

        print("Invoker: Does anybody want something done after I finish?")
        if isinstance(self._on_finish, CommandInterface):
            self._on_finish.execute()


if __name__ == "__main__":
    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Say Hi!"))
    receiver = Receiver()
    invoker.set_on_finish(ComplexCommand(
        receiver, "Send email", "Save report"))

    invoker.do_something_important()
