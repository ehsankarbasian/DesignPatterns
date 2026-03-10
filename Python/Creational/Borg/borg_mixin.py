
# Implement state sharing in a mixin and use it anywhere
class SharedStateMixin:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


# How to use
class Logger(SharedStateMixin):
    pass

class Config(SharedStateMixin):
    pass
