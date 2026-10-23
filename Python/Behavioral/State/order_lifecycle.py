"""
Order lifecycle modeled with explicit state objects and documented coordination options.

This module is domain-focused. The public API is the Order context. Callers should not
instantiate or depend on concrete states. The context delegates domain actions to its
current state object.

State transition coordination options

    Context-directed transitions (context knows concrete states)
        The context decides which concrete state comes next and assigns it directly.
        States focus on behavior but do not own the transition graph.

        Trade-offs:
            - Simple for small graphs and small teams.
            - High coupling: context must reference every concrete state class.
            - Transition rules drift into the context and become conditional logic.
            - Adding a state often requires editing the context.

    State-directed transitions with explicit next-state return (state returns next)
        Each action returns either the same state instance or the next state instance.
        The context applies the returned state.

        Trade-offs:
            - Transition rules stay close to the behavior that triggers them.
            - Context remains stable while transitions evolve.
            - Testing is straightforward: verify returned state type and invariants.
            - Requires discipline: callers must not depend on concrete states.

    State-directed transitions by calling a context transition method (state calls go-to)
        Each action can call order.transition_to(...) directly to move the context.
        This keeps the context thin and makes transitions explicit at the call site.

        Trade-offs:
            - Explicit transitions with low boilerplate in the context.
            - Concrete states depend on the context type, reducing portability.
            - Works well when the aggregate root is the natural transition owner.

    Hierarchical transitions (only higher-level states know sub-states)
        States are grouped into super-states. A super-state manages transitions among
        its internal sub-states. External code sees only the super-state boundary and
        does not depend on sub-state types.

        Trade-offs:
            - Keeps transition knowledge local to a scope and scales better.
            - Avoids a single centralized transition map as the lifecycle grows.
            - Increases indirection and class count; boundaries must be crisp.

Encapsulation notes
    Encapsulation here focuses on hiding concrete state types from callers and localizing
    transition rules near the behavior that requires them. The context exposes stable domain
    actions; concrete states remain internal details.

This file implements the state-directed transitions by calling a context transition method.
Trade-offs:
    - Increases the number of objects compared to a conditional-only implementation.
    - Reduces branching complexity and improves locality of change as the domain evolves.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class InvalidStateTransitionError(RuntimeError):
    """
    Raised when a domain action is not supported by the current lifecycle state.

    Trade-offs:
        - Exceptions create a strict failure mode that forces the caller to handle invalid flows.
        - Alternative designs include returning Result objects, which can reduce try/except noise
          but may spread conditional checks across callers.
    """

    pass


# State interface
class OrderStateInterface(ABC):

    @abstractmethod
    def pay(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def ship(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def deliver(self, order: "Order") -> None:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, order: "Order") -> None:
        raise NotImplementedError


# Concrete state
class PendingState(OrderStateInterface):

    def pay(self, order: "Order") -> None:
        order.transition_to(PaidState())

    def ship(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cannot ship before payment.")

    def deliver(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cannot deliver before shipping.")

    def cancel(self, order: "Order") -> None:
        order.transition_to(CancelledState())


# Concrete state
class PaidState(OrderStateInterface):

    def pay(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Payment is already completed.")

    def ship(self, order: "Order") -> None:
        order.transition_to(ShippedState())

    def deliver(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cannot deliver before shipping.")

    def cancel(self, order: "Order") -> None:
        order.transition_to(CancelledState())


# Concrete state
class ShippedState(OrderStateInterface):

    def pay(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Order is already paid and shipped.")

    def ship(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Order is already shipped.")

    def deliver(self, order: "Order") -> None:
        order.transition_to(DeliveredState())

    def cancel(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cannot cancel while in transit.")


# Concrete state
class DeliveredState(OrderStateInterface):

    def pay(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Delivered orders are immutable.")

    def ship(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Delivered orders are immutable.")

    def deliver(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Delivered orders are immutable.")

    def cancel(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Delivered orders are immutable.")


# Concrete state
class CancelledState(OrderStateInterface):

    def pay(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cancelled orders are immutable.")

    def ship(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cancelled orders are immutable.")

    def deliver(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cancelled orders are immutable.")

    def cancel(self, order: "Order") -> None:
        raise InvalidStateTransitionError("Cancelled orders are immutable.")


# Context
class Order:

    def __init__(self, order_id: str, initial_state: OrderStateInterface | None = None) -> None:
        self.order_id = order_id
        self._state: OrderStateInterface = initial_state or PendingState()

    @property
    def state_name(self) -> str:
        return self._state.__class__.__name__

    def transition_to(self, new_state: OrderStateInterface) -> None:
        """
        Replace the active state object.

        This method is the single mutation point for lifecycle transitions. Keeping state
        replacement in one place makes it easy to add instrumentation, auditing, or domain
        guards later without spreading that logic across every concrete state.
        """
        self._state = new_state

    def pay(self) -> None:
        self._state.pay(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)


if __name__ == "__main__":
    # Success path: an order moves through the typical lifecycle steps.
    order = Order("ORD-1001")
    print(f"{order.order_id} -> {order.state_name}")

    order.pay()
    print(f"{order.order_id} -> {order.state_name}")

    order.ship()
    print(f"{order.order_id} -> {order.state_name}")

    order.deliver()
    print(f"{order.order_id} -> {order.state_name}")

    # Failure path: attempting an invalid transition raises an exception.
    invalid_order = Order("ORD-1002")
    print(f"{invalid_order.order_id} -> {invalid_order.state_name}")

    try:
        invalid_order.ship()
    except InvalidStateTransitionError as exc:
        print(f"Expected error: {exc}")
