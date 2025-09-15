from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime


# Mediator Interface
class ChatRoomMediatorInterface(ABC):
    
    @abstractmethod
    def show_message(user: User, message: str):
        pass


# Concrete Mediator
class ChatRoom(ChatRoomMediatorInterface):
    
    def show_message(self, user, message):
        time = datetime.now()
        sender = user.name
        print(f'{time} [{sender}] {message}')


# Colleagues
class User:
    
    def __init__(self, name: str, chat_mediator: ChatRoomMediatorInterface):
        self._name = name
        self._chat_mediator = chat_mediator
    
    @property
    def name(self) -> str:
        return self._name
    
    def send(self, message: str):
        self._chat_mediator.show_message(self, message)


if __name__ == "__main__":
    mediator = ChatRoom()
    
    zoor_avar = User('Zoor Avar', mediator)
    singham = User('Singham', mediator)
    
    zoor_avar.send('Meow')
    singham.send('Roaaaar !')
