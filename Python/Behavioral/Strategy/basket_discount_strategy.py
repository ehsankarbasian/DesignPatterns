"""
This module implements a Strategy-based discount mechanism for a shopping basket.

Design goal
This file intentionally models a discount subsystem that resembles real-world enterprise codebases
where discount rules evolve, require multiple domain signals, and must remain extensible without
causing tight coupling between pricing rules and basket implementations.

Key decisions
1) Context passing (not data passing)
   Discount strategies receive a context object instead of a small set of primitive inputs.
   This supports strategies that may require multiple signals such as basket gross amount,
   loyalty level, item composition, customer tier, campaign eligibility, and future pricing metadata.

2) Interface Segregation for contexts
   Strategies depend on small, role-based interfaces (context interfaces) that expose only what a strategy needs.
   This prevents broad coupling and reduces the risk of a Cartesian dependency explosion where each
   strategy expects a different concrete basket type.

3) Naming: gross_amount vs subtotal
   "subtotal" can be ambiguous across domains and teams. "gross_amount" is chosen to explicitly
   represent the basket value before discounts, taxes, shipping fees, or other adjustments.
   The complementary concept is typically "net_amount" for the final payable amount, but this module
   focuses on computing discounts only.

When this approach is justified
This design is useful when:
- You anticipate multiple basket-like contexts (web basket, POS invoice, B2B quote, draft order).
- Strategies evolve frequently and may need additional inputs over time.
- You want strategies to remain reusable across different contexts as long as the required role-based
  interface is satisfied.

When this approach is unnecessary
If your domain is simple and stable, for example:
- You have exactly one basket type and do not expect additional contexts.
- Discount rules are small, stable, and depend on only one or two primitive inputs.
Then a simpler design can be sufficient:
- Data passing (e.g., passing a Decimal gross amount) may be clearer.
- A single context interface may be acceptable and cheaper in cognitive overhead.

Trade-offs
Benefits:
- Better extensibility without forcing unrelated changes across strategies.
- Reduced coupling between strategies and concrete basket implementations.

Costs:
- More types and indirection, which increases cognitive load.
- Slightly more ceremony for small projects.

Monetary calculations
All monetary values use Decimal to avoid floating-point inaccuracies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable


# Value Object

@dataclass(frozen=True)
class BasketItem:
    """
    Represents an immutable line item within a shopping basket.

    Uses Decimal for all monetary properties to prevent precision loss.
    """

    sku: str
    name: str
    unit_price: Decimal
    quantity: int

    @property
    def gross_amount(self) -> Decimal:
        """
        Calculates the line item total amount before discounts or other adjustments.
        """

        return self.unit_price * Decimal(self.quantity)


# Context Interface

class GrossPricedContextInterface(ABC):
    """
    Exposes gross pricing information needed by strategies calculating discounts on gross total.
    """

    @property
    @abstractmethod
    def gross_amount(self) -> Decimal:
        """
        Total monetary amount of the basket before any deductions, taxes, or shipping fees.
        """

        raise NotImplementedError


# Context Interface

class LoyaltyEligibleBasketContextInterface(GrossPricedContextInterface, ABC):
    """
    Exposes customer loyalty metrics in conjunction with baseline gross pricing.
    """

    @property
    @abstractmethod
    def loyalty_level(self) -> int:
        """
        Customer tier or loyalty score used for discount qualification.
        """

        raise NotImplementedError


# Context Interface

class SkuAwareBasketContextInterface(GrossPricedContextInterface, ABC):
    """
    Exposes basket line items for strategies requiring SKU inspection.
    """

    @property
    @abstractmethod
    def items(self) -> tuple[BasketItem, ...]:
        """
        Immutable collection of items present in the basket.
        """

        raise NotImplementedError


# Strategy Interface

class DiscountStrategyInterface(ABC):
    """
    Defines the interface for discount calculation strategies receiving a context view.
    """

    @abstractmethod
    def calculate_discount(self, context: GrossPricedContextInterface) -> Decimal:
        """
        Computes the discount reduction based on the provided context view.
        """

        raise NotImplementedError


# Concrete Context

class Basket(LoyaltyEligibleBasketContextInterface, SkuAwareBasketContextInterface):
    """
    Acts as the Aggregate Root managing line items, customer loyalty, and invariant enforcement.

    Invariants
    - Discount deductions can never result in a negative final payable amount.
    - Calculated discount cannot exceed total basket gross amount.
    """

    def __init__(self, items: Iterable[BasketItem], loyalty_level: int) -> None:
        self._items = tuple(items)
        self._loyalty_level = loyalty_level

    @property
    def items(self) -> tuple[BasketItem, ...]:
        """
        Provides read-only access to contained line items.
        """

        return self._items

    @property
    def loyalty_level(self) -> int:
        """
        Returns the loyalty rating bound to this basket instance.
        """

        return self._loyalty_level

    @property
    def gross_amount(self) -> Decimal:
        """
        Aggregates the gross sum across all active line items.
        """

        return sum((item.gross_amount for item in self._items), start=Decimal("0"))

    def discounted_amount(self, strategy: DiscountStrategyInterface) -> Decimal:
        """
        Applies a pricing strategy and enforces core financial invariants on the result.
        """

        discount_amount = strategy.calculate_discount(self)
        if discount_amount < Decimal("0"):
            raise ValueError("discount_amount must not be negative.")
        if discount_amount > self.gross_amount:
            discount_amount = self.gross_amount
        return self.gross_amount - discount_amount


# Concrete Strategy

class PercentageOfGrossAmountDiscountStrategy(DiscountStrategyInterface):
    """
    Computes a uniform percentage-based discount across the basket gross amount.
    """

    def __init__(self, percentage: Decimal) -> None:
        if percentage < Decimal("0"):
            raise ValueError("percentage must be non-negative.")
        self._percentage = percentage

    def calculate_discount(self, context: GrossPricedContextInterface) -> Decimal:
        """
        Returns percentage reduction derived strictly from the gross amount.
        """

        return (context.gross_amount * self._percentage) / Decimal("100")


class LoyaltyPercentageDiscountStrategy(DiscountStrategyInterface):
    """
    Computes a percentage-based discount conditionally applied when loyalty thresholds are met.
    """

    def __init__(self, minimum_loyalty_level: int, percentage: Decimal) -> None:
        if minimum_loyalty_level < 0:
            raise ValueError("minimum_loyalty_level must be non-negative.")
        if percentage < Decimal("0"):
            raise ValueError("percentage must be non-negative.")
        self._minimum_loyalty_level = minimum_loyalty_level
        self._percentage = percentage

    def calculate_discount(self, context: GrossPricedContextInterface) -> Decimal:
        """
        Returns calculated percentage discount if loyalty level satisfies the required threshold.
        """

        if not isinstance(context, LoyaltyEligibleBasketContextInterface):
            raise TypeError("context must implement LoyaltyEligibleBasketContextInterface.")

        if context.loyalty_level < self._minimum_loyalty_level:
            return Decimal("0")
        return (context.gross_amount * self._percentage) / Decimal("100")


class SkuFixedAmountDiscountStrategy(DiscountStrategyInterface):
    """
    Computes a flat monetary reduction if any designated target SKU is present in the basket.

    This strategy applies the discount once if at least one matching SKU exists.
    It does not multiply the discount by the number of matching items.
    """

    def __init__(self, target_skus: set[str], fixed_discount_amount: Decimal) -> None:
        if not target_skus:
            raise ValueError("target_skus must not be empty.")
        if fixed_discount_amount < Decimal("0"):
            raise ValueError("fixed_discount_amount must be non-negative.")
        self._target_skus = set(target_skus)
        self._fixed_discount_amount = fixed_discount_amount

    def calculate_discount(self, context: GrossPricedContextInterface) -> Decimal:
        """
        Returns the fixed discount if any matching SKU exists; otherwise returns zero.
        """

        if not isinstance(context, SkuAwareBasketContextInterface):
            raise TypeError("context must implement SkuAwareBasketContextInterface.")

        if any(item.sku in self._target_skus for item in context.items):
            return self._fixed_discount_amount
        return Decimal("0")


if __name__ == "__main__":
    basket = Basket(
        items=[
            BasketItem(sku="KB-001", name="Keyboard", unit_price=Decimal("50.00"), quantity=1),
            BasketItem(sku="MS-002", name="Mouse", unit_price=Decimal("25.00"), quantity=2),
        ],
        loyalty_level=3,
    )

    percentage_strategy = PercentageOfGrossAmountDiscountStrategy(percentage=Decimal("10"))
    loyalty_strategy = LoyaltyPercentageDiscountStrategy(minimum_loyalty_level=2, percentage=Decimal("15"))
    sku_strategy = SkuFixedAmountDiscountStrategy(
        target_skus={"KB-001"},
        fixed_discount_amount=Decimal("7.50"),
    )

    print("Gross amount:", basket.gross_amount)
    print("Discounted amount (percentage):", basket.discounted_amount(percentage_strategy))
    print("Discounted amount (loyalty):", basket.discounted_amount(loyalty_strategy))
    print("Discounted amount (sku fixed):", basket.discounted_amount(sku_strategy))
