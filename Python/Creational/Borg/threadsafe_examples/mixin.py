import threading

from typing import Any


class ThreadSafeBorgMixin:
    """
    Mixin providing:
    - Borg shared state
    - Thread-safe access via a central lock
    """

    _shared_state: dict[str, Any] = {}
    _lock = threading.RLock()

    def __init__(self, *args, **kwargs) -> None:
        self.__dict__ = self._shared_state
        super().__init__(*args, **kwargs)

    def set_shared(self, key: str, value: Any) -> None:
        with self._lock:
            self.__dict__[key] = value

    def get_shared(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self.__dict__.get(key, default)


# How to use
class AppConfig(ThreadSafeBorgMixin):
    # Concrete class using ThreadSafeBorgMixin

    def __init__(self, name: str):
        # In Borg (Monostate), all instance attributes become shared because all instances share the same __dict__
        super().__init__()
        self.name = name
