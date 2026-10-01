"""
Design goal:
    Demonstrate and contrast the two classic implementations of the GoF Adapter Pattern:
    1. Class Adapter (Structural Inheritance / Multiple Inheritance).
    2. Object Adapter (Structural Composition / Delegation).

Key decisions:
    - Use a single, realistic Logging Domain scenario to benchmark both variants side-by-side.
    - Define Target as an abstract role interface (ModernLogger) expected by Client.
    - Define Adaptee as a Legacy Syslog client with incompatible signatures and severity levels.
    - Implement Class Adapter via multiple inheritance (Target + Adaptee).
    - Implement Object Adapter via composition (Target wrapping an Adaptee instance).

Trade-offs:
    - Class Adapter:
        + Can directly override Adaptee internal/protected hooks without boilerplate wrappers.
        + Only one object allocated in memory (no delegation indirection overhead).
        - Tightly couples the adapter to a concrete Adaptee class at compile-time.
        - Leaks Adaptee public methods into Target namespace (violating Interface Segregation).
        - Cannot adapt multiple runtime subclasses of Adaptee dynamically.
    - Object Adapter:
        + Loosely coupled; works with Adaptee and all its polymorphic subclasses polymorphically.
        + Keeps Target interface completely clean (encapsulates Adaptee internals).
        - Introduces an extra level of indirection (attribute lookup & method call overhead).
        - Cannot override Adaptee behavior easily without subclassing Adaptee separately.

When justified:
    - Class Adapter: When working in Python where multiple inheritance is supported, and you explicitly
      need to override Adaptee protected behaviors or require seamless `isinstance(adapter, Adaptee)` checks.
    - Object Adapter: The standard production default; when you want decoupling, runtime flexibility,
      and adherence to Composition Over Inheritance.

When unnecessary:
    - When Adaptee can be modified directly (no closed 3rd-party code).
    - When a simple functional transformation or wrapper function suffices without polymorphism.
"""

from abc import ABC, abstractmethod
from typing import Any, Mapping


# Target
class ModernLogger(ABC):

    @abstractmethod
    def log(self, level: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        pass


# Adaptee
class LegacySyslogService:

    SEVERITY_MAP = {
        "DEBUG": 7,
        "INFO": 6,
        "WARNING": 4,
        "ERROR": 3,
        "CRITICAL": 2,
    }

    def send_raw_log(self, severity_code: int, raw_payload: str) -> None:
        print(f"[Syslog Daemon | Severity {severity_code}] -> {raw_payload}")

    def _format_legacy_prefix(self, message: str) -> str:
        return f"HOST_APP: {message}"


# Class Adapter
class ClassLoggerAdapter(ModernLogger, LegacySyslogService):
    """
    Adapts LegacySyslogService to ModernLogger via multiple inheritance.
    Directly accesses Adaptee methods and constants as part of its own class hierarchy.
    """

    def log(self, level: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        severity = self.SEVERITY_MAP.get(level.upper(), 6)
        prefixed_message = self._format_legacy_prefix(message)
        payload = f"{prefixed_message} | Context: {context}" if context else prefixed_message
        self.send_raw_log(severity, payload)


# Object Adapter
class ObjectLoggerAdapter(ModernLogger):
    """
    Adapts LegacySyslogService to ModernLogger via composition.
    Wraps an Adaptee instance and delegates logging calls through structural indirection.
    """

    def __init__(self, adaptee: LegacySyslogService) -> None:
        self._adaptee = adaptee

    def log(self, level: str, message: str, context: Mapping[str, Any] | None = None) -> None:
        severity = self._adaptee.SEVERITY_MAP.get(level.upper(), 6)
        payload = f"{message} | Context: {context}" if context else message
        self._adaptee.send_raw_log(severity, payload)


# Client
def run_client(logger: ModernLogger) -> None:
    logger.log("INFO", "User login successful", {"user_id": 1042})
    logger.log("ERROR", "Database connection timeout", {"retry_count": 3})


if __name__ == "__main__":
    # Class Adapter demonstration
    class_adapter = ClassLoggerAdapter()
    run_client(class_adapter)
    print(f"Is Class Adapter an instance of LegacySyslogService? {isinstance(class_adapter, LegacySyslogService)}")

    # Object Adapter demonstration
    legacy_instance = LegacySyslogService()
    object_adapter = ObjectLoggerAdapter(adaptee=legacy_instance)
    run_client(object_adapter)
    print(f"Is Object Adapter an instance of LegacySyslogService? {isinstance(object_adapter, LegacySyslogService)}")
