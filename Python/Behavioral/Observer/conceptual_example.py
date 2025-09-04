from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


# Code from: https://refactoring.guru/design-patterns/observer/python/example

# Publisher
class Subject(ABC):
    # A set of methods for managing subscribers.

    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class ConcreteSubject(Subject):
    _state: int = None
    _observers: List[Observer] = []

    def attach(self, observer: Observer):
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    # Trigger an update in each subscriber.
    def notify(self):
        
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self):
        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)

        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()


# Subscriber
class Observer(ABC):
    # The update method is used by subjects.

    @abstractmethod
    def update(self, subject: Subject):
        pass


class ConcreteObserverA(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state < 3:
            print("ConcreteObserverA: Reacted to the event")


class ConcreteObserverB(Observer):
    def update(self, subject: Subject) -> None:
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB: Reacted to the event")


if __name__ == "__main__":
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()
    
    subject = ConcreteSubject()
    subject.attach(observer_a)
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()
    subject.detach(observer_a)
    subject.some_business_logic()
