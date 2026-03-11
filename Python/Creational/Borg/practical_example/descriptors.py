from threading import RLock


class SharedField:
    """
    Descriptor implementing thread-safe shared state.
    The value is stored once and shared across all instances of the owning class.
    """

    def __init__(self, default=None):
        self.default = default
        self._value = default
        self._lock = RLock()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        with self._lock:
            return self._value

    def __set__(self, instance, value):
        with self._lock:
            self._value = value

    def __delete__(self, instance):
        with self._lock:
            self._value = self.default
