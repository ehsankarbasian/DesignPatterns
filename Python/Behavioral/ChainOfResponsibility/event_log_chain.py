from __future__ import annotations
import re
from typing import Optional, Pattern, Dict, Any


# Example from book: Clean Code in Python - Season 9

class Event:
    """
    Design goal:
        Process log lines along a chain using regex matching and Null Object termination.
    Key decisions:
        Default successor to NullEvent to eliminate conditional successor verification.
    Trade-offs:
        Requires regex evaluation before delegating processing down the chain.
    """

    pattern: Optional[Pattern[str]] = None

    def __init__(self, next_event: Optional[Event] = None) -> None:
        self.successor: Event = next_event if next_event is not None else NullEvent()

    def process(self, logline: str) -> Dict[str, Any]:
        if self.can_process(logline):
            return self._process(logline)

        return self.successor.process(logline)

    def _process(self, logline: str) -> Dict[str, Any]:
        parsed_data = self._parse_data(logline)
        return {
            "type": self.__class__.__name__,
            "id": parsed_data.get("id"),
            "value": parsed_data.get("value"),
        }

    @classmethod
    def can_process(cls, logline: str) -> bool:
        return cls.pattern is not None and cls.pattern.match(logline) is not None

    @classmethod
    def _parse_data(cls, logline: str) -> Dict[str, str]:
        if cls.pattern is None:
            return {}

        if (parsed := cls.pattern.match(logline)) is not None:
            return parsed.groupdict()

        return {}


class NullEvent(Event):
    """
    Design goal:
        Act as a terminal event handler that safely returns an empty payload.
    Key decisions:
        Bypass the base constructor to avoid recursive NullEvent instantiation and
        point successor at itself so repeated delegation stays safe.
    Trade-offs:
        Inherits unused class methods from Event base class.
    """

    def __init__(self) -> None:
        self.successor: Event = self

    def process(self, logline: str) -> Dict[str, Any]:
        return {}


class LoginEvent(Event):
    pattern = re.compile(r"(?P<id>\d+):\s+login\s+(?P<value>\S+)")


class LogoutEvent(Event):
    pattern = re.compile(r"(?P<id>\d+):\s+logout\s+(?P<value>\S+)")


if __name__ == "__main__":
    chain = LoginEvent(
        next_event=LogoutEvent()
    )

    logs = [
        "101: login ehsan_k",
        "102: logout ehsan_k",
        "103: unknown_action data",
    ]

    print("--- Processing Logs ---")
    for log in logs:
        result = chain.process(log)

        if result:
            print(f"Processed: {result}")
        else:
            print(f"Ignored: '{log}' (No handler found)")
