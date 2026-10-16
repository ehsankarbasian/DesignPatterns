"""
Purpose:
    Decouple object consumers from concrete instantiation logic.
    Allow dynamic runtime configuration through cloneable prototypes.

Mechanism:
    Maintain a name-to-prototype mapping inside a centralized manager.
    Return independent cloned instances on demand using deep duplication.
    Expose existence check, registration, removal, and retrieval seams.

Setup and use:
    Configure instances once at application boot inside the registry.
    Query prototypes solely by identifier and interface contract during execution.
    Isolate nested mutable state so mutations never affect stored baselines.

Trade-offs
    Deep copying preserves state safety for nested structures at slight CPU cost.
    Lookup relies on runtime string keys instead of static compile-time symbols.
    Independent allocations prevent implicit sharing of read-only cached resources.
"""


from __future__ import annotations


"""
Gang of Four Motivation:
    A reusable editor framework provides tools for creating graphical objects.
    Application-specific graphics should not require matching tool subclasses
    whose only distinction is the concrete object they construct.

Client parameterization:
    A creation tool receives a configured prototype through the prototype
    interface. Each creation request clones that prototype, initializes the
    instance-specific state, and inserts the new object into the document.
    The tool depends on the cloning contract rather than concrete constructors.

Reduced subclassing:
    Different instances of the same tool class can hold different prototypes.
    This reduces the need for a parallel hierarchy of creation tools while
    preserving concrete graphic classes where their behavior differs.
    The setup code still selects and constructs the initial prototypes.

Registry connection:
    Direct injection supplies a client with a particular prototype.
    A prototype manager extends this arrangement by maintaining named
    prototypes that clients can select at runtime.

    WidgetRegistry demonstrates this management mechanism: setup code registers
    configured widgets, and client code requests clones through registry keys.
    The registry centralizes prototype lookup without changing the underlying
    creation principle: new objects originate from existing instances.

Cloning policy:
    Prototype does not prescribe shallow copying or deep copying.
    The implementation defines which state is duplicated and which references
    remain shared. This example uses deep copying to isolate mutable widget
    configuration between a prototype and its clones.

Trade-offs
    Direct prototype injection keeps a client's creation dependency explicit.
    A registry supports runtime selection but introduces key management and
    missing-prototype handling. Neither mechanism removes the need to establish
    valid initial prototypes or define suitable clone initialization.
"""


import copy
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class UnknownPrototypeError(KeyError):
    """
    Raised when a requested prototype key does not exist in the registry.
    """


class WidgetPrototypeInterface(ABC):
    """
    Abstract interface defining the clone contract for all widget prototypes.
    """

    @abstractmethod
    def clone(self) -> WidgetPrototypeInterface:
        """
        Return a distinct copy of this prototype instance.
        """


@dataclass
class ChartWidget(WidgetPrototypeInterface):
    """
    Concrete chart widget holding mutable visualization settings.
    """

    title: str
    chart_type: str
    refresh_interval: int
    filters: list[str] = field(default_factory=list)

    def clone(self) -> ChartWidget:
        return copy.deepcopy(self)


@dataclass
class TableWidget(WidgetPrototypeInterface):
    """
    Concrete table widget containing nested column and formatting state.
    """

    title: str
    refresh_interval: int
    columns: list[str] = field(default_factory=list)
    settings: dict[str, str] = field(default_factory=dict)

    def clone(self) -> TableWidget:
        return copy.deepcopy(self)


class WidgetRegistry:
    """
    Prototype manager maintaining registered prototypes and issuing clones.
    """

    def __init__(self) -> None:
        self._prototypes: dict[str, WidgetPrototypeInterface] = {}

    def register(self, name: str, prototype: WidgetPrototypeInterface) -> None:
        self._prototypes[name] = prototype

    def unregister(self, name: str) -> None:
        self._prototypes.pop(name, None)

    def clone(self, name: str) -> WidgetPrototypeInterface:
        try:
            return self._prototypes[name].clone()
        except KeyError:
            raise UnknownPrototypeError(
                f"No prototype registered under the name {name!r}"
            ) from None

    def contains(self, name: str) -> bool:
        return name in self._prototypes


if __name__ == "__main__":
    registry = WidgetRegistry()

    registry.register("sales-chart", ChartWidget(
        title="Sales Overview",
        chart_type="line",
        refresh_interval=60,
        filters=["region", "quarter"],
    ))
    registry.register("orders-table", TableWidget(
        title="Recent Orders",
        refresh_interval=30,
        columns=["id", "customer", "total"],
        settings={"page_size": "25", "sortable": "true"},
    ))

    first = registry.clone("sales-chart")
    second = registry.clone("sales-chart")
    table = registry.clone("orders-table")

    first.title = "Q3 Sales Overview"
    first.filters.append("channel")
    first.refresh_interval = 15

    table.columns.append("status")
    table.settings["page_size"] = "50"

    print("clones are distinct objects:", first is not second)
    print("second keeps its own title:", second.title)
    print("second keeps its own filters:", second.filters)
    print("stored prototype untouched:", registry.clone("sales-chart").filters)
    print("table clone got its own columns:", table.columns)
    print("registry still holds sales-chart:", registry.contains("sales-chart"))

    registry.unregister("orders-table")
    print("contains after unregister:", registry.contains("orders-table"))

    try:
        registry.clone("orders-table")
    except UnknownPrototypeError as error:
        print("unknown key error:", error)
