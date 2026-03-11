import threading

from typing import Any


class ThreadSafeBorgBasic:
    # Borg with centralized lock protecting the entire shared state.

    _shared_state: dict[str, Any] = {}
    _lock = threading.RLock()

    def __init__(self) -> None:
        self.__dict__ = self._shared_state

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self.__dict__[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self.__dict__.get(key, default)
