"""
Specification Design Pattern (Magic Methods Implementation)

Composes specifications using Python dunder methods (__and__, __or__, __invert__).
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass

    def __and__(self, other: "Specification[T]") -> "Specification[T]":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification[T]") -> "Specification[T]":
        return OrSpecification(self, other)

    def __invert__(self) -> "Specification[T]":
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class OrSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class NotSpecification(Specification[T]):
    def __init__(self, wrapped: Specification[T]) -> None:
        self._wrapped = wrapped

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._wrapped.is_satisfied_by(candidate)


class Customer:
    def __init__(
        self,
        name: str,
        credit_score: int,
        is_email_verified: bool,
        is_banned: bool,
        is_vip: bool,
    ) -> None:
        self.name = name
        self.credit_score = credit_score
        self.is_email_verified = is_email_verified
        self.is_banned = is_banned
        self.is_vip = is_vip


class MinimumCreditScoreSpecification(Specification[Customer]):
    def __init__(self, minimum_score: int) -> None:
        self._minimum_score = minimum_score

    def is_satisfied_by(self, candidate: Customer) -> bool:
        return candidate.credit_score >= self._minimum_score


class EmailVerifiedSpecification(Specification[Customer]):
    def is_satisfied_by(self, candidate: Customer) -> bool:
        return candidate.is_email_verified


class BannedUserSpecification(Specification[Customer]):
    def is_satisfied_by(self, candidate: Customer) -> bool:
        return candidate.is_banned


class VipCustomerSpecification(Specification[Customer]):
    def is_satisfied_by(self, candidate: Customer) -> bool:
        return candidate.is_vip


if __name__ == "__main__":
    alice = Customer(name="Alice", credit_score=720, is_email_verified=True, is_banned=False, is_vip=False)
    bob = Customer(name="Bob", credit_score=450, is_email_verified=True, is_banned=False, is_vip=True)
    charlie = Customer(name="Charlie", credit_score=800, is_email_verified=False, is_banned=True, is_vip=False)

    has_good_credit = MinimumCreditScoreSpecification(minimum_score=700)
    is_verified = EmailVerifiedSpecification()
    is_banned = BannedUserSpecification()
    is_vip = VipCustomerSpecification()

    # Rule: (Verified AND Good Credit) AND NOT Banned
    standard_loan_policy = is_verified & has_good_credit & ~is_banned

    # Rule: Standard policy OR VIP customer
    flexible_loan_policy = standard_loan_policy | is_vip

    print(f"Alice standard loan: {standard_loan_policy.is_satisfied_by(alice)}")
    print(f"Bob standard loan: {standard_loan_policy.is_satisfied_by(bob)}")
    print(f"Bob flexible loan: {flexible_loan_policy.is_satisfied_by(bob)}")
    print(f"Charlie flexible loan: {flexible_loan_policy.is_satisfied_by(charlie)}")
