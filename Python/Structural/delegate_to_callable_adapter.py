"""
Design goal:
Provide a pluggable Adapter that converts heterogeneous Adaptees into a uniform Target
without modifying either the Client or the Adaptees.

Key decisions:
- Show a delegate-object Adapter variant first (explicit adapter objects).
- Evolve to a parameterized callable Adapter variant (first-class functions).

When justified:
- Delegate objects: when adaptation needs state, caching, configuration, or multi-step logic.
- Parameterized callables: when adaptation is pure/stateless and boilerplate is undesirable.

When unnecessary:
- When Adaptees already match the Target interface or can be normalized upstream.

Trade-offs:
- Delegate objects improve discoverability and encapsulation but increase object count and boilerplate.
- Callables reduce ceremony and are highly composable but can hide structure if overused.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


# Target
@dataclass(frozen=True, slots=True)
class ExportRow:
    """Target consumed by the Client."""

    key: str
    summary: str


# Adaptee
@dataclass(frozen=True, slots=True)
class SensorReading:
    """An Adaptee with a schema that does not match the Target."""

    sensor_id: str
    temperature_c: float
    humidity_percent: float


# Adaptee
@dataclass(frozen=True, slots=True)
class LogEntry:
    """Another Adaptee with a different schema that does not match the Target."""

    source: str
    severity: str
    message: str


# Target Interface
class ExportRowSourceInterface(ABC):
    """Target-facing interface for heterogeneous Adaptees."""

    @abstractmethod
    def export_key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def export_summary(self) -> str:
        raise NotImplementedError


# Client
class ExportClient:
    """Client that only understands the Target (ExportRow)."""

    def export(self, rows: Iterable[ExportRow]) -> str:
        parts: list[str] = []
        for row in rows:
            parts.append(f"{row.key}\t{row.summary}")
        return "\n".join(parts)


# Initial approach: Delegate Object Adapter
# Encapsulates transformation within explicit dedicated adapter instances.

# Delegate Adapter Interface
class ExportRowDelegateAdapterInterface(ABC):
    """
    Delegate Adapter interface.

    Trade-offs (localized):
    - Pros: explicit objects, clear discoverability, easy to attach state/configuration.
    - Cons: more classes and instances, repetitive boilerplate for simple adaptations.
    """

    @abstractmethod
    def to_export_row(self, adaptee: ExportRowSourceInterface) -> ExportRow:
        raise NotImplementedError


# Delegate Adapter
class SensorReadingDelegateAdapter(ExportRowDelegateAdapterInterface):
    """Delegate Adapter for SensorReading."""

    def to_export_row(self, adaptee: ExportRowSourceInterface) -> ExportRow:
        return ExportRow(key=adaptee.export_key(), summary=adaptee.export_summary())


# Delegate Adapter
class LogEntryDelegateAdapter(ExportRowDelegateAdapterInterface):
    """Delegate Adapter for LogEntry."""

    def to_export_row(self, adaptee: ExportRowSourceInterface) -> ExportRow:
        return ExportRow(key=adaptee.export_key(), summary=adaptee.export_summary())


# Wrapper Adapter (Adaptee -> Target Interface)
class SensorReadingTargetAdapter(ExportRowSourceInterface):
    """Adapter that exposes SensorReading through the Target interface."""

    def __init__(self, adaptee: SensorReading) -> None:
        self._adaptee = adaptee

    def export_key(self) -> str:
        return f"sensor:{self._adaptee.sensor_id}"

    def export_summary(self) -> str:
        t = self._adaptee.temperature_c
        h = self._adaptee.humidity_percent
        return f"temp_c={t:.1f}; humidity_pct={h:.1f}"


# Wrapper Adapter (Adaptee -> Target Interface)
class LogEntryTargetAdapter(ExportRowSourceInterface):
    """Adapter that exposes LogEntry through the Target interface."""

    def __init__(self, adaptee: LogEntry) -> None:
        self._adaptee = adaptee

    def export_key(self) -> str:
        return f"log:{self._adaptee.source}:{self._adaptee.severity}"

    def export_summary(self) -> str:
        return self._adaptee.message


# Client-facing facade (delegate-object variant)
class DelegatingExportService:
    """
    Client-facing facade using delegate objects.

    Trade-offs (localized):
    - Delegate objects are justified if each adaptation needs state/configuration/caching.
    - For pure mapping, this service becomes ceremony-heavy.
    """

    def __init__(self, client: ExportClient, adapter: ExportRowDelegateAdapterInterface) -> None:
        self._client = client
        self._adapter = adapter

    def export(self, sources: Sequence[ExportRowSourceInterface]) -> str:
        rows = [self._adapter.to_export_row(src) for src in sources]
        return self._client.export(rows)


# Refactoring starting point: Parameterized Callable Adapter
# Replaces boilerplate delegate adapter classes with pure, first-class callables.

# Parameterized Callable type alias
RecordFormatter = Callable[[ExportRowSourceInterface], ExportRow]


# Parameterized Callable Adapter (function)
def default_export_row_formatter(source: ExportRowSourceInterface) -> ExportRow:
    """
    Parameterized callable Adapter.

    Functional evolution:
    Replaces dedicated delegate adapter classes with a first-class pure callable.
    Adaptees conforming to ExportRowSourceInterface are projected directly into ExportRow.

    Trade-offs (localized):
    - Pros: eliminates boilerplate classes and object instantiation for stateless mappings.
    - Cons: cannot encapsulate mutable adaptation state or multi-step caching without closures.
    """
    return ExportRow(key=source.export_key(), summary=source.export_summary())


# Client-facing facade (callable variant)
class CallableExportService:
    """
    Client-facing facade using a parameterized callable Adapter.

    Key decision (localized):
    - The adaptation behavior is injected as a first-class callable rather than an object instance.
    """

    def __init__(self, client: ExportClient, formatter: RecordFormatter) -> None:
        self._client = client
        self._formatter = formatter

    def export(self, sources: Sequence[ExportRowSourceInterface]) -> str:
        rows = [self._formatter(src) for src in sources]
        return self._client.export(rows)


def _build_sources() -> list[ExportRowSourceInterface]:
    s1 = SensorReading(sensor_id="A1", temperature_c=21.25, humidity_percent=44.9)
    s2 = SensorReading(sensor_id="B7", temperature_c=19.80, humidity_percent=52.3)
    l1 = LogEntry(source="auth", severity="WARN", message="token nearing expiry")
    l2 = LogEntry(source="api", severity="ERROR", message="upstream timeout")

    return [
        SensorReadingTargetAdapter(s1),
        SensorReadingTargetAdapter(s2),
        LogEntryTargetAdapter(l1),
        LogEntryTargetAdapter(l2),
    ]


if __name__ == "__main__":
    client = ExportClient()
    sources = _build_sources()

    # Delegate object approach: Instantiate explicit adapter classes per stream.
    # Justified when transformations require state, caching, or custom configuration.
    delegating_sensor = DelegatingExportService(client, SensorReadingDelegateAdapter())
    delegating_log = DelegatingExportService(client, LogEntryDelegateAdapter())

    sensor_only = [s for s in sources if s.export_key().startswith("sensor:")]
    log_only = [s for s in sources if s.export_key().startswith("log:")]

    out_sensor_delegate = delegating_sensor.export(sensor_only)
    out_log_delegate = delegating_log.export(log_only)

    # Parameterized callable approach: Pass a pure function eliminating boilerplate classes.
    # Refactored for stateless transformations where behavior injection suffices.
    callable_service = CallableExportService(client, default_export_row_formatter)
    out_all_callable = callable_service.export(sources)

    assert "sensor:A1\ttemp_c=21.2; humidity_pct=44.9" in out_sensor_delegate
    assert "sensor:B7\ttemp_c=19.8; humidity_pct=52.3" in out_sensor_delegate

    assert "log:auth:WARN\ttoken nearing expiry" in out_log_delegate
    assert "log:api:ERROR\tupstream timeout" in out_log_delegate

    assert "sensor:A1\ttemp_c=21.2; humidity_pct=44.9" in out_all_callable
    assert "log:api:ERROR\tupstream timeout" in out_all_callable

    # Parameterized callable variant using an inline lambda expression.
    # Demonstrates maximum brevity and flexible on-the-fly client adaptation.
    out_all_callable_lambda = CallableExportService(
        client,
        lambda src: ExportRow(key=src.export_key(), summary=src.export_summary()),
    ).export(sources)

    assert out_all_callable_lambda == out_all_callable
