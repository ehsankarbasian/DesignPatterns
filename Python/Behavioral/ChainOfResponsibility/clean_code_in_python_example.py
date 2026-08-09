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


if __name__ == "__main__":
    # Client: Assemble the chain of responsibility.
    # We chain LoginEvent to LogoutEvent.
    chain = LoginEvent(
        next_event=LogoutEvent()
    )

    # Some sample log lines to process.
    logs = [
        "101: login ehsan_k",
        "102: logout ehsan_k",
        "103: unknown_action data",
    ]

    print("--- Processing Logs ---")
    for log in logs:
        # The client only interacts with the head of the chain.
        result = chain.process(log)
        
        if result:
            print(f"Processed: {result}")
        else:
            # If no one in the chain could process it.
            print(f"Ignored: '{log}' (No handler found)")

    # Explanation:
    # 1. '101: login' is matched by LoginEvent (first in chain).
    # 2. '102: logout' is passed by LoginEvent to LogoutEvent and matched there.
    # 3. '103: unknown' travels through the whole chain and returns an empty dict.
