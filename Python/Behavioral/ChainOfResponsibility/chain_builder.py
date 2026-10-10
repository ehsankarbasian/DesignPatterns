"""Fluent builder that wires a string-pipeline chain and appends its terminator."""

from future import annotations

from abc import ABC, abstractmethod
from functools import reduce
from typing import List, Optional, Type


# Base link; owns successor storage and the forwarding mechanics.
# Concrete handlers only decide: consume here, or forward via _call_next.
class Handler(ABC):
    """Process a request or forward it to the successor."""

    def init(self) -> None:
        self._successor: Optional["Handler"] = None

    def set_successor(self, successor: Optional["Handler"]) -> None:
        self._successor = successor

    def _call_next(self, request: str) -> str:
        if self._successor is None:
            return request
        return self._successor.handle(request)

    @abstractmethod
    def handle(self, request: str) -> str:
        raise NotImplementedError


# Terminal link; absorbs the tail so no successor call ever returns None.
class NullHandler(Handler):
    """Return the request unchanged as the chain's default outcome."""

    def set_successor(self, successor: Optional["Handler"]) -> None:
        del successor  # chain ends here by design

    def handle(self, request: str) -> str:
        return request


# First stage; strips surrounding whitespace, then forwards.
class TrimHandler(Handler):
    """Trim the request and delegate the rest downstream."""

    def handle(self, request: str) -> str:
        return self._call_next(request.strip())


# Second stage; uppercases the text, then forwards.
class UppercaseHandler(Handler):
    """Uppercase the request and delegate the rest downstream."""

    def handle(self, request: str) -> str:
        return self._call_next(request.upper())


# Fluent assembler; links handlers pairwise with one fold and terminates.
# One instance assembles one chain; handlers are mutated during build.
class ChainBuilder:
    """Accumulate handlers, wire them, append NullHandler, return head."""

    def init(self) -> None:
        self._handlers: List[Handler] = []

    def with_handler(self, handler: Handler) -> "ChainBuilder":
        self._handlers.append(handler)
        return self

    def with_handler_type(self, handler_type: Type[Handler]) -> "ChainBuilder":
        return self.with_handler(handler_type())

    def build(self) -> Handler:
        if not self._handlers:
            raise ValueError("cannot build a chain with no handlers")

        def link(left: Handler, right: Handler) -> Handler:
            left.set_successor(right)
            return right

        reduce(link, self._handlers)
        self._handlers[-1].set_successor(NullHandler())
        return self._handlers[0]


if name == "main":
    chain = (
        ChainBuilder()
        .with_handler_type(TrimHandler)
        .with_handler_type(UppercaseHandler)
        .build()
    )
    print(chain.handle("  hello chain builder  "))
