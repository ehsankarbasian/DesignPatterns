"""
Specification Design Pattern (Simple Implementation)

Provides a single atomic interface to encapsulate business validation rules.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass


class UserAccount:
    def __init__(self, username: str, age: int, is_active: bool) -> None:
        self.username = username
        self.age = age
        self.is_active = is_active


class MinimumAgeSpecification(Specification[UserAccount]):
    def __init__(self, minimum_age: int) -> None:
        self._minimum_age = minimum_age

    def is_satisfied_by(self, candidate: UserAccount) -> bool:
        return candidate.age >= self._minimum_age


class ActiveAccountSpecification(Specification[UserAccount]):
    def is_satisfied_by(self, candidate: UserAccount) -> bool:
        return candidate.is_active


if __name__ == "__main__":
    alice = UserAccount(username="alice", age=22, is_active=True)
    bob = UserAccount(username="bob", age=16, is_active=False)

    adult_rule = MinimumAgeSpecification(minimum_age=18)
    active_rule = ActiveAccountSpecification()

    print(adult_rule.is_satisfied_by(alice))
    print(adult_rule.is_satisfied_by(bob))
    print(active_rule.is_satisfied_by(alice))
