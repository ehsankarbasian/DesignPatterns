"""
Advanced Borg / Monostate implementation using a mixin.

Design goals:
- Cooperative multiple inheritance
- Per-class shared state (Not per mixin)
- Safe with subclassing
- Production friendly
"""

from typing import Any


class SharedStateMixin:
    """
    Advanced Borg / Monostate mixin.

    - Cooperative multiple inheritance
    - Per-class shared state
    - Preserves attributes set by other base classes
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls = self.__class__

        if "_shared_state" not in cls.__dict__:
            cls._shared_state = {}

        # Preserve attributes created during super().__init__
        instance_state = self.__dict__
        cls._shared_state.update(instance_state)
        self.__dict__ = cls._shared_state
