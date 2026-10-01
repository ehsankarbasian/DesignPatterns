"""
Design goal:
    Demonstrate an idiomatic functional Strategy pattern using first-class callables
    and typing.Protocol, eliminating class boilerplate for stateless logic.

Key decisions:
    1. Structural contract: Define DiscountStrategy as a Protocol with __call__.
    2. Closures for parameterized logic: Higher-order functions generate dynamic strategies.
    3. Domain invariants in dataclasses: Enforce invariants in __post_init__ of frozen dataclasses
       (DDD-aligned; Value Object-like validation at construction time).
    4. Context invariance: Order enforces monetary rounding and clamping independently.

Trade-offs:
    - Best suited for pure, stateless, mathematical algorithms.
    - Not suitable for enterprise architectures requiring nominal typing (ABC), internal mutable state, or multi-method lifecycles.
    - Protocol verifies callability structurally via @runtime_checkable, but runtime signature enforcement requires static analysis (mypy).
    - Accepting float in quantize_money is a convenience trade-off; strict monetary domains should exclusively use Decimal or str.
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol, Sequence, runtime_checkable

PENNY = Decimal("0.01")


def quantize_money(value: str | float | int | Decimal) -> Decimal:
    """
    Format and round monetary amounts to two decimal places.
    """

    return Decimal(str(value)).quantize(PENNY, rounding=ROUND_HALF_UP)


# Domain models

@dataclass(frozen=True)
class OrderItem:
    """
    Immutable order line item.

    Domain invariants are strictly enforced in __post_init__ at construction time
    to prevent invalid domain state (DDD Value Object semantic).
    """

    sku: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if self.unit_price < Decimal("0"):
            raise ValueError(f"Unit price cannot be negative: {self.unit_price}")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive: {self.quantity}")

    @property
    def total_price(self) -> Decimal:
        return (self.unit_price * Decimal(self.quantity)).quantize(PENNY, rounding=ROUND_HALF_UP)


# Strategy interface

@runtime_checkable
class DiscountStrategy(Protocol):
    """
    Callable structural protocol for stateless discount calculation.

    runtime_checkable allows structural isinstance checks, but full signature validation
    is deferred to static type analysis (mypy).
    """

    def __call__(self, gross_total: Decimal, item_count: int, loyalty_tier: int) -> Decimal:
        ...


# Concrete strategies

def flat_rate_discount(gross_total: Decimal, item_count: int, loyalty_tier: int) -> Decimal:
    """
    Stateless pure function strategy: 10.00 discount for orders >= 100.00.
    """

    if gross_total >= Decimal("100.00"):
        return quantize_money("10.00")
    return Decimal("0.00")


def percentage_discount_factory(rate: Decimal) -> DiscountStrategy:
    """
    Higher-order factory closure for parameterized percentage discounts.
    """

    if not (Decimal("0") <= rate <= Decimal("1.0")):
        raise ValueError(f"Discount rate must be between 0.0 and 1.0: {rate}")

    def strategy(gross_total: Decimal, item_count: int, loyalty_tier: int) -> Decimal:
        return (gross_total * rate).quantize(PENNY, rounding=ROUND_HALF_UP)

    return strategy


def loyalty_tiered_discount(gross_total: Decimal, item_count: int, loyalty_tier: int) -> Decimal:
    """
    Stateless pure function strategy: Tiered discount based on customer loyalty.
    """

    if loyalty_tier <= 0:
        return Decimal("0.00")
    rates = {1: Decimal("0.05"), 2: Decimal("0.10")}
    rate = rates.get(loyalty_tier, Decimal("0.15"))
    return (gross_total * rate).quantize(PENNY, rounding=ROUND_HALF_UP)


# Context

@dataclass(frozen=True)
class Order:
    """
    Context executing stateless discount callables and guarding domain invariants.
    """

    items: tuple[OrderItem, ...]
    loyalty_tier: int = 0

    @classmethod
    def create(cls, items: Sequence[OrderItem], loyalty_tier: int = 0) -> Order:
        if loyalty_tier < 0:
            raise ValueError(f"Loyalty tier cannot be negative: {loyalty_tier}")
        return cls(items=tuple(items), loyalty_tier=loyalty_tier)

    @property
    def gross_total(self) -> Decimal:
        return sum((item.total_price for item in self.items), start=Decimal("0.00"))

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)

    def calculate_discount(self, strategy: DiscountStrategy) -> Decimal:
        """
        Execute strategy callable with defensive financial invariant guards.
        """

        if not callable(strategy):
            raise TypeError("Strategy must be a callable.")
        raw_discount = strategy(self.gross_total, self.item_count, self.loyalty_tier)
        clamped_discount = max(Decimal("0.00"), min(raw_discount, self.gross_total))
        return clamped_discount.quantize(PENNY, rounding=ROUND_HALF_UP)

    def net_total(self, strategy: DiscountStrategy) -> Decimal:
        """
        Calculate final net amount after applying discount.
        """

        return (self.gross_total - self.calculate_discount(strategy)).quantize(PENNY, rounding=ROUND_HALF_UP)


if __name__ == "__main__":
    items = [
        OrderItem(sku="CLEAN-PYTHON", unit_price=quantize_money("50.00"), quantity=2),
        OrderItem(sku="SOFTWARE-ARCH", unit_price=quantize_money("60.00"), quantity=1),
    ]
    order = Order.create(items=items, loyalty_tier=2)

    print(f"Gross Total: {order.gross_total} | Item Count: {order.item_count}")
    assert order.gross_total == Decimal("160.00")
    assert order.item_count == 3

    # Flat discount
    flat_discount = order.calculate_discount(flat_rate_discount)
    print(f"Flat Discount applied: {flat_discount} -> Net: {order.net_total(flat_rate_discount)}")
    assert flat_discount == Decimal("10.00")
    assert order.net_total(flat_rate_discount) == Decimal("150.00")

    # Factory closure (20%)
    twenty_percent = percentage_discount_factory(Decimal("0.20"))
    twenty_discount = order.calculate_discount(twenty_percent)
    print(f"Percentage (20%) applied: {twenty_discount} -> Net: {order.net_total(twenty_percent)}")
    assert twenty_discount == Decimal("32.00")
    assert order.net_total(twenty_percent) == Decimal("128.00")

    # Loyalty tiered (Tier 2 = 10%)
    loyalty_discount = order.calculate_discount(loyalty_tiered_discount)
    print(f"Loyalty Tier 2 applied: {loyalty_discount} -> Net: {order.net_total(loyalty_tiered_discount)}")
    assert loyalty_discount == Decimal("16.00")
    assert order.net_total(loyalty_tiered_discount) == Decimal("144.00")

    # Inline lambda strategy
    bulk_promo: DiscountStrategy = lambda gross, count, tier: quantize_money("5.00") if count >= 3 else Decimal("0.00")
    bulk_discount = order.calculate_discount(bulk_promo)
    print(f"Lambda Promo applied: {bulk_discount} -> Net: {order.net_total(bulk_promo)}")
    assert bulk_discount == Decimal("5.00")

    # Invariant Clamping: Excessive discount capped at gross total
    overkill_promo: DiscountStrategy = lambda gross, count, tier: Decimal("999.00")
    clamped_discount = order.calculate_discount(overkill_promo)
    print(f"Overkill Promo clamped: {clamped_discount} -> Net: {order.net_total(overkill_promo)}")
    assert clamped_discount == Decimal("160.00")
    assert order.net_total(overkill_promo) == Decimal("0.00")

    # Structural protocol conformity
    assert isinstance(flat_rate_discount, DiscountStrategy)
    assert isinstance(twenty_percent, DiscountStrategy)
    assert isinstance(loyalty_tiered_discount, DiscountStrategy)

    print("\nAll functional strategy calculations and protocol checks verified successfully!")
