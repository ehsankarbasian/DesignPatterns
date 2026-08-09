from __future__ import annotations

import re
from typing import Optional, Pattern


class Event:
    
    # Shared regex pattern for all concrete events.
    pattern: Optional[Pattern[str]] = None


    def __init__(self, next_event: Optional[Event] = None) -> None:
        self.successor = next_event


    def process(self, logline: str) -> dict:
        # Try to handle the log line in the current handler.
        if self.can_process(logline):
            return self._process(logline)

        # Otherwise delegate to the next handler in the chain.
        if self.successor is not None:
            return self.successor.process(logline)

        return {}


    def _process(self, logline: str) -> dict:
        parsed_data = self._parse_data(logline)
        return {
            "type": self.__class__.__name__,
            "id": parsed_data["id"],
            "value": parsed_data["value"],
        }


    @classmethod
    def can_process(cls, logline: str) -> bool:
        # A handler can process only if its pattern matches the input.
        return cls.pattern is not None and cls.pattern.match(logline) is not None


    @classmethod
    def _parse_data(cls, logline: str) -> dict:
        
        # Extract named groups from the matching log line.
        if cls.pattern is None:
            return {}

        if (parsed := cls.pattern.match(logline)) is not None:
            return parsed.groupdict()

        return {}


class LoginEvent(Event):
    pattern = re.compile(r"(?P<id>\d+):\s+login\s+(?P<value>\S+)")


class LogoutEvent(Event):
    pattern = re.compile(r"(?P<id>\d+):\s+logout\s+(?P<value>\S+)")



