from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


# Code from: https://refactoring.guru/design-patterns/observer/python/example

# Defines interface for attaching, detaching, and notifying observers.
# Target Subject Interface
class SubjectInterface(ABC):
    """Abstract base definition for observable domain subjects."""

    @abstractmethod
    def attach(self, observer: ObserverInterface) -> None:
        pass

    @abstractmethod
    def detach(self, observer: ObserverInterface) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


# Defines state updates and notification dispatching logic.
# Concrete Subject Component
class ConcreteSubject(SubjectInterface):
    """Maintains state and dispatches notifications upon state updates.
    
    Trade-offs
        Directly embeds observer list management instead of delegating subscription tracking.
    """

    def __init__(self) -> None:
        self._state: int = 0
        self._observers: List[ObserverInterface] = []

    def attach(self, observer: ObserverInterface) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print("Subject: Attached an observer.")

    def detach(self, observer: ObserverInterface) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print("Subject: Detached an observer.")

    def notify(self) -> None:
        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)
        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()


# Defines interface for reacting to state changes in subjects.
# Target Observer Interface
class ObserverInterface(ABC):
    """Abstract base definition for event subscriber components."""

    @abstractmethod
    def update(self, subject: SubjectInterface) -> None:
        pass


# Reacts to state changes when subject state evaluates below threshold.
# Concrete Observer Component
class ConcreteObserverA(ObserverInterface):
    """Subscriber that filters notifications based on low subject state values."""

    def update(self, subject: SubjectInterface) -> None:
        if isinstance(subject, ConcreteSubject) and subject._state < 3:
            print("ConcreteObserverA: Reacted to the event.")


# Reacts to state changes when subject state matches specific ranges.
# Concrete Observer Component
class ConcreteObserverB(ObserverInterface):
    """Subscriber that filters notifications based on boundary subject state values."""

    def update(self, subject: SubjectInterface) -> None:
        if isinstance(subject, ConcreteSubject) and (subject._state == 0 or subject._state >= 2):
            print("ConcreteObserverB: Reacted to the event.")


if __name__ == "__main__":
    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()

    subject.attach(observer_a)
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()
