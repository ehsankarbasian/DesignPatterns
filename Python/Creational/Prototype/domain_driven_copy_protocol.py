from __future__ import annotations

"""
TODO

Domain-driven copy protocol establishing enterprise clone semantics.

Design goal:
Bridge Python's low-level copy protocols (__copy__ and __deepcopy__) with rich
Domain-Driven Design (DDD) aggregate semantics, replacing mechanical object-graph
duplication with explicit business-boundary policies. The existing
custom_copy_protocol.py solely demonstrates cycle resolution via memoization on
generic Component primitives, lacking invariant preservation, lifecycle state
resets, audit separation, and shared reference boundaries required in enterprise
systems.

Key decisions:
- Select an Enterprise Order Aggregate domain containing an Aggregate Root
  (Order), child entities with parent back-references (OrderLine), shared master
  data references (CustomerRef, ProductCatalog), and domain lifecycle states
  (Draft, Paid, Shipped).
- Identity recreation: Clone operations must invalidate and regenerate aggregate
  root IDs, line item IDs, and external tracking tokens to prevent cross-entity
  identity collisions.
- Lifecycle state reset: Completed or terminal aggregate states (Paid, Fulfilled)
  must transition back to an initial mutable state (Draft) upon duplication.
- Audit decoupling: Creation timestamps, version counters, and audit logs must
  reinitialize rather than carry historical provenance into the cloned entity.
- Hybrid reference copying: Differentiate between immutable catalog/profile data
  (kept shallow/shared to optimize memory) and aggregate state (deeply cloned
  with memoization to resolve back-references safely).

Trade-offs:
    Coupling deep copy logic directly to domain models introduces operational
    maintenance overhead as entity attributes evolve, contrasting with blind
    reflection-based cloners. However, this explicit approach guarantees domain
    invariants, eliminates shared mutation bugs, and strictly enforces valid
    business lifecycle boundaries.
"""


"""
Domain topology and semantic boundaries for aggregate graph replication.

Domain entities and structural topology:
- Aggregate Root (Order):
    Encapsulates transaction identity, customer association, lifecycle status
    (DRAFT, SUBMITTED, PAID, SHIPPED, CANCELLED), audit tracking, and monetary totals.
- Child Entity (OrderLine):
    Maintains line item identity, catalog linkage, quantity, price invariants,
    and a cyclical back-reference to its owning Order aggregate.
- Shared Master Context (CustomerProfile & ProductCatalogItem):
    Immutable master data referenced across multiple aggregate boundaries that
    must retain shared identity and prevent entity divergence.

Business policies for domain replication:
- Identity regeneration:
    Cloned aggregates and contained entities must generate fresh identifiers to
    prevent transactional identity collisions across distinct orders.
- Lifecycle and audit sanitization:
    Duplicating an order in terminal or committed states forces an automatic
    reset to DRAFT, reinitializes timestamps, and strips payment or tracking tokens.
- Hybrid reference demarcation:
    Distinguishes aggregate-internal state (deeply duplicated) from external
    master data references (retained as shallow shared references).
- Cyclical graph integrity:
    Parent-child bidirectional links must be rebound to the new aggregate instance
    without reference leaks to the source aggregate.

Trade-offs:
    Enforcing aggregate duplication policies directly on domain entities increases
    domain model surface area, but guarantees that business invariants and lifecycle
    boundaries remain strictly preserved during reordering workflows.
"""


import copy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum, auto
from typing import Iterable, Optional
from uuid import UUID, uuid4


# Order lifecycle state enumeration
# Value object, lifecycle invariant boundary
class OrderStatus(Enum):
    """
    Lifecycle states permissible within the order aggregate.
    """

    DRAFT = auto()
    SUBMITTED = auto()
    PAID = auto()
    SHIPPED = auto()
    CANCELLED = auto()


# Customer master record identity reference
# Read-only shared context node, master data reference
@dataclass(frozen=True, slots=True)
class CustomerProfile:
    """
    Customer entity reference maintained outside aggregate boundary.
    """

    customer_id: UUID
    legal_name: str
    tax_id: str


# Commercial catalog product reference
# Read-only catalog node, shared flyweight payload
@dataclass(frozen=True, slots=True)
class ProductCatalogItem:
    """
    Catalog specification referenced across orders.
    """

    sku: str
    name: str
    base_price: Decimal
    is_discontinued: bool = False


# Line item entity bound to order aggregate
# Child entity node, cyclical aggregate participant
@dataclass(slots=True)
class OrderLine:
    """
    Individual line item encapsulating product quantity and monetary total.
    """

    line_id: UUID
    catalog_item: ProductCatalogItem
    quantity: int
    unit_price: Decimal
    order: Optional["Order"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        """
        Validate line item domain invariants upon initialization.
        """

        if self.quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self.unit_price < Decimal("0"):
            raise ValueError("Unit price cannot be negative.")

    def line_total(self) -> Decimal:
        """
        Calculate total price contribution of this line item.
        """

        return self.unit_price * self.quantity

    def __deepcopy__(self, memo: dict) -> "OrderLine":
        """
        Replicate child entity adhering to aggregate boundary rules.

        Trade-offs:
            Explicit field-by-field replication requires manual updates when new
            entity fields are introduced, but ensures zero unintentional leakage.
        """

        existing = memo.get(id(self))
        if existing is not None:
            return existing

        cloned = OrderLine(
            line_id=uuid4(),
            catalog_item=self.catalog_item,
            quantity=self.quantity,
            unit_price=self.unit_price,
            order=None,
        )
        memo[id(self)] = cloned

        if self.order is not None:
            cloned.order = copy.deepcopy(self.order, memo)

        return cloned


# Commercial order aggregate root entity
# Aggregate root anchor, transactional consistency boundary
@dataclass(slots=True)
class Order:
    """
    Consistency boundary managing lines, audit state, and lifecycle progression.
    """

    order_id: UUID
    customer: CustomerProfile
    status: OrderStatus
    lines: list[OrderLine] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    payment_reference: Optional[str] = None
    external_tracking_token: Optional[str] = None

    @classmethod
    def create_draft(cls, customer: CustomerProfile) -> "Order":
        """
        Factory method instantiating a clean mutable order draft.
        """

        return cls(
            order_id=uuid4(),
            customer=customer,
            status=OrderStatus.DRAFT,
            lines=[],
            created_at=datetime.now(timezone.utc),
            version=1,
            payment_reference=None,
            external_tracking_token=None,
        )

    def add_line(self, catalog_item: ProductCatalogItem, quantity: int) -> OrderLine:
        """
        Append a product line item maintaining bidirectional integrity.
        """

        line = OrderLine(
            line_id=uuid4(),
            catalog_item=catalog_item,
            quantity=quantity,
            unit_price=catalog_item.base_price,
            order=self,
        )
        self.lines.append(line)
        return line

    def total(self) -> Decimal:
        """
        Aggregate total price across active line items.
        """

        return sum((line.line_total() for line in self.lines), Decimal("0"))

    def iter_discontinued_items(self) -> Iterable[ProductCatalogItem]:
        """
        Inspect line items identifying obsolete catalog references.
        """

        for line in self.lines:
            if line.catalog_item.is_discontinued:
                yield line.catalog_item

    def _reset_lifecycle_for_clone(self) -> None:
        """
        Sanitize operational state and audit fields for duplicated aggregate.
        """

        self.status = OrderStatus.DRAFT
        self.payment_reference = None
        self.external_tracking_token = None
        self.created_at = datetime.now(timezone.utc)
        self.version = 1

    def __deepcopy__(self, memo: dict) -> "Order":
        """
        Replicate aggregate root executing domain boundary policies.

        Trade-offs:
            Direct implementation within the entity introduces protocol coupling,
            avoiding external cloner services while enforcing aggregate rules.
        """

        existing = memo.get(id(self))
        if existing is not None:
            return existing

        cloned = Order(
            order_id=uuid4(),
            customer=self.customer,
            status=self.status,
            lines=[],
            created_at=datetime.now(timezone.utc),
            version=1,
            payment_reference=None,
            external_tracking_token=None,
        )
        memo[id(self)] = cloned

        cloned.lines = [copy.deepcopy(line, memo) for line in self.lines]
        for line in cloned.lines:
            line.order = cloned

        cloned._reset_lifecycle_for_clone()
        return cloned

    def clone(self) -> "Order":
        """
        Domain entry point triggering policy-driven duplication protocol.
        """

        return copy.deepcopy(self)


# Architectural notes:
# - Post-clone reconciliation workflows (e.g. inventory reservation checks and
#   discontinued catalog item substitutions) belong to application coordination
#   services to keep the domain entity free from transactional I/O concerns.
# - The memo dictionary ensures that cyclic references between Order and OrderLine
#   bind strictly to newly allocated instances without graph leakage.
