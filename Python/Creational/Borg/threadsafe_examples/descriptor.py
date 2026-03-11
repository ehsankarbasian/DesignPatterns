import threading
from typing import Any


# Define shared_attr logic according to descriptor protocol
class ThreadSafeSharedAttribute:
    """
    Descriptor for thread-safe shared attributes.

    The value is stored on the descriptor itself, so it is shared across
    all instances of the owning class.
    """

    def __init__(self, initial_value: Any = None) -> None:
        self._value = initial_value
        self._lock = threading.RLock()

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if instance is None:
            return self

        with self._lock:
            return self._value

    def __set__(self, instance: Any, value: Any) -> None:
        with self._lock:
            self._value = value

    def __delete__(self, instance: Any) -> None:
        raise AttributeError("Cannot delete a shared attribute")
        

class BorgBase:
    """
    Basic Borg base class.

    All instances share the same instance dictionary.
    """
    _shared_state: dict[str, Any] = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state


# How to use
class ApplicationConfig(BorgBase):
    """
    Example Borg using thread-safe descriptors for selected attributes.
    """
    db_url = ThreadSafeSharedAttribute("sqlite:///default.db")
    debug = ThreadSafeSharedAttribute(False)
    pool_size = ThreadSafeSharedAttribute(5)
