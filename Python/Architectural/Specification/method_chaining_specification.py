"""
Specification Design Pattern (Method Chaining Implementation)

Demonstrates fluent method chaining for business rules where operations
represent domain workflows and cannot be mapped to boolean operators.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class OrderEvent:
    def __init__(self, step_name: str, is_successful: bool) -> None:
        self.step_name = step_name
        self.is_successful = is_successful


class ChainedSpecification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass

    def then_verify(self, next_specification: "ChainedSpecification[T]") -> "ChainedSpecification[T]":
        return SequenceSpecification(self, next_specification)

    def when_condition(self, condition_specification: "ChainedSpecification[T]") -> "ChainedSpecification[T]":
        return ConditionalSpecification(condition_specification, self)


class SequenceSpecification(ChainedSpecification[List[OrderEvent]]):
    def __init__(
        self,
        first_specification: ChainedSpecification[List[OrderEvent]],
        next_specification: ChainedSpecification[List[OrderEvent]],
    ) -> None:
        self._first_specification = first_specification
        self._next_specification = next_specification

    def is_satisfied_by(self, candidate: List[OrderEvent]) -> bool:
        return (
            self._first_specification.is_satisfied_by(candidate)
            and self._next_specification.is_satisfied_by(candidate)
        )


class ConditionalSpecification(ChainedSpecification[List[OrderEvent]]):
    def __init__(
        self,
        condition_specification: ChainedSpecification[List[OrderEvent]],
        target_specification: ChainedSpecification[List[OrderEvent]],
    ) -> None:
        self._condition_specification = condition_specification
        self._target_specification = target_specification

    def is_satisfied_by(self, candidate: List[OrderEvent]) -> bool:
        if self._condition_specification.is_satisfied_by(candidate):
            return self._target_specification.is_satisfied_by(candidate)
        return True


class StepCompletedSpecification(ChainedSpecification[List[OrderEvent]]):
    def __init__(self, step_name: str) -> None:
        self._step_name = step_name

    def is_satisfied_by(self, candidate: List[OrderEvent]) -> bool:
        return any(event.step_name == self._step_name and event.is_successful for event in candidate)


class PremiumCustomerSpecification(ChainedSpecification[List[OrderEvent]]):
    def __init__(self, is_premium: bool) -> None:
        self._is_premium = is_premium

    def is_satisfied_by(self, candidate: List[OrderEvent]) -> bool:
        return self._is_premium


if __name__ == "__main__":
    order_history = [
        OrderEvent(step_name="INVENTORY_RESERVED", is_successful=True),
        OrderEvent(step_name="PAYMENT_PROCESSED", is_successful=True),
        OrderEvent(step_name="EXPEDITED_SHIPPING", is_successful=True),
    ]

    inventory_rule = StepCompletedSpecification(step_name="INVENTORY_RESERVED")
    payment_rule = StepCompletedSpecification(step_name="PAYMENT_PROCESSED")
    shipping_rule = StepCompletedSpecification(step_name="EXPEDITED_SHIPPING")
    is_premium_user = PremiumCustomerSpecification(is_premium=True)

    pipeline_rule = (
        inventory_rule
        .then_verify(payment_rule)
        .then_verify(shipping_rule.when_condition(is_premium_user))
    )

    print(pipeline_rule.is_satisfied_by(order_history))
