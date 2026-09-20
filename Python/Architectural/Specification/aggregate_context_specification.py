"""
Specification Design Pattern (Aggregate Decision Context)

1. The Architectural Problem (Why not validate single entities directly?):
--------------------------------------------------------------------------
In Domain-Driven Design (DDD), complex business rules often transcend a single
entity boundary. For example, evaluating whether an order can be fulfilled
requires validating:
  - The Customer (state, suspension, KYC status)
  - The Order/Cart (item counts, total amount)
  - The Inventory Snapshot (stock availability per SKU)
  - Financial Ledger (wallet balance or credit limit)

Passing isolated entities (e.g., passing Customer to a Cart specification) creates
tight coupling between disjoint aggregates and breaks TypeVar safety in
Specification[T].

2. The Solution (Decision Context / Aggregate Boundary):
--------------------------------------------------------
We introduce an explicit Decision Context (`OrderFulfillmentContext`). This object
acts as an immutable evaluation boundary (Snapshot/Projection) containing all
necessary state required to make an aggregate-level domain decision.

All atomic and composite specifications evaluate against this single candidate:
Specification[OrderFulfillmentContext].

3. Architectural Trade-offs (Pros & Cons):
------------------------------------------
PROS:
  - Strong Type Safety: Generic[T] candidates remain strictly typed.
  - Decoupled Entities: Customer and Inventory models know nothing about each other.
  - High Composability: Pure Boolean algebra (&, |, ~) across multi-entity rules.
  - Testability: Context snapshots can be mocked or instantiated without DB state.

CONS:
  - Data Assembly Overhead: The application service layer must query and assemble
    the context snapshot before evaluating the specification.
  - State Staleness Risk: Snapshot evaluations assume data does not mutate during
    in-memory verification (requires transactional consistency at execution time).
"""

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class AbstractSpecification(ABC, Generic[T]):
    """
    Abstract base specification providing operator-overloaded composite methods.
    
    Subclasses must implement `is_satisfied_by`. Logical operators (__and__,
    __or__, __invert__) return composite specification trees evaluated at runtime.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Evaluates domain rule against the candidate."""
        pass

    def __and__(self, other: "AbstractSpecification[T]") -> "AbstractSpecification[T]":
        return AndSpecification(self, other)

    def __or__(self, other: "AbstractSpecification[T]") -> "AbstractSpecification[T]":
        return OrSpecification(self, other)

    def __invert__(self) -> "AbstractSpecification[T]":
        return NotSpecification(self)


class AndSpecification(AbstractSpecification[T]):
    """Composite node representing logical conjunction (A AND B). Short-circuits evaluation."""

    def __init__(self, left: AbstractSpecification[T], right: AbstractSpecification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class OrSpecification(AbstractSpecification[T]):
    """Composite node representing logical disjunction (A OR B). Short-circuits evaluation."""

    def __init__(self, left: AbstractSpecification[T], right: AbstractSpecification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class NotSpecification(AbstractSpecification[T]):
    """Composite node representing logical negation (NOT A)."""

    def __init__(self, wrapped: AbstractSpecification[T]) -> None:
        self._wrapped = wrapped

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._wrapped.is_satisfied_by(candidate)


# ----------------------------------------------------------------------
# Domain Entities and Value Objects (Disjoint Aggregates)
# ----------------------------------------------------------------------


class Customer:
    """Represents the buying actor within the identity/customer boundary."""

    def __init__(self, customer_id: str, is_active: bool, is_suspended: bool) -> None:
        self.customer_id = customer_id
        self.is_active = is_active
        self.is_suspended = is_suspended


class OrderItem:
    """Value object inside the sales/order boundary."""

    def __init__(self, product_sku: str, quantity: int, unit_price: float) -> None:
        self.product_sku = product_sku
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


class StockReservation:
    """Snapshot projection from the warehouse/inventory boundary."""

    def __init__(self, product_sku: str, available_units: int) -> None:
        self.product_sku = product_sku
        self.available_units = available_units


# ----------------------------------------------------------------------
# Aggregate Context (The Unified Candidate for Specification[T])
# ----------------------------------------------------------------------


class OrderFulfillmentContext:
    """
    Cohesive Decision Context that unifies multi-aggregate states into an immutable snapshot.
    
    Why this boundary exists:
    Cross-aggregate policies cannot belong to a single entity without violating single
    responsibility. This context encapsulates all variables needed to decide whether
    an order can proceed to fulfillment.
    """

    def __init__(
        self,
        customer: Customer,
        order_items: List[OrderItem],
        stock_reservations: List[StockReservation],
        wallet_balance: float,
    ) -> None:
        self.customer = customer
        self.order_items = order_items
        self.inventory_map = {item.product_sku: item.available_units for item in stock_reservations}
        self.wallet_balance = wallet_balance

    @property
    def order_grand_total(self) -> float:
        """Calculates computed monetary total across all order line items."""
        return sum(item.total_price for item in self.order_items)


# ----------------------------------------------------------------------
# Atomic Context Specifications
# ----------------------------------------------------------------------


class ActiveCustomerSpecification(AbstractSpecification[OrderFulfillmentContext]):
    """Validates that the customer account is in an active, non-suspended state."""

    def is_satisfied_by(self, candidate: OrderFulfillmentContext) -> bool:
        return candidate.customer.is_active and not candidate.customer.is_suspended


class NonEmptyOrderSpecification(AbstractSpecification[OrderFulfillmentContext]):
    """Ensures fulfillment cannot process a cart/order with zero items."""

    def is_satisfied_by(self, candidate: OrderFulfillmentContext) -> bool:
        return len(candidate.order_items) > 0


class SufficientInventorySpecification(AbstractSpecification[OrderFulfillmentContext]):
    """
    Validates inventory consistency:
    Checks if every ordered SKU has enough quantity reserved in the inventory snapshot.
    """

    def is_satisfied_by(self, candidate: OrderFulfillmentContext) -> bool:
        for item in candidate.order_items:
            stock = candidate.inventory_map.get(item.product_sku, 0)
            if item.quantity > stock:
                return False
        return True


class SufficientFundsSpecification(AbstractSpecification[OrderFulfillmentContext]):
    """Validates financial solvency: Wallet balance must meet or exceed order total."""

    def is_satisfied_by(self, candidate: OrderFulfillmentContext) -> bool:
        return candidate.wallet_balance >= candidate.order_grand_total


# ----------------------------------------------------------------------
# Client Usage and Policy Composition
# ----------------------------------------------------------------------

if __name__ == "__main__":
    alice = Customer(customer_id="cust-101", is_active=True, is_suspended=False)
    items = [
        OrderItem(product_sku="BOOK-DDD", quantity=1, unit_price=60.0),
        OrderItem(product_sku="BOOK-DDIA", quantity=2, unit_price=45.0),
    ]
    warehouse_stock = [
        StockReservation(product_sku="BOOK-DDD", available_units=5),
        StockReservation(product_sku="BOOK-DDIA", available_units=10),
    ]

    # Context A: Solvent balance (200 >= 150), valid stock, active user
    valid_context = OrderFulfillmentContext(
        customer=alice,
        order_items=items,
        stock_reservations=warehouse_stock,
        wallet_balance=200.0,
    )

    # Context B: Underfunded balance (100 < 150)
    underfunded_context = OrderFulfillmentContext(
        customer=alice,
        order_items=items,
        stock_reservations=warehouse_stock,
        wallet_balance=100.0,
    )

    # Complex Business Policy:
    # An order can be fulfilled IF customer is active AND order has items
    # AND warehouse has stock AND wallet has sufficient funds.
    order_fulfillment_policy = (
        ActiveCustomerSpecification()
        & NonEmptyOrderSpecification()
        & SufficientInventorySpecification()
        & SufficientFundsSpecification()
    )

    print(f"Valid context satisfies policy: {order_fulfillment_policy.is_satisfied_by(valid_context)}")
    print(f"Underfunded context satisfies policy: {order_fulfillment_policy.is_satisfied_by(underfunded_context)}")
