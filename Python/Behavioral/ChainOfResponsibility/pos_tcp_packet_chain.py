"""Routes POS TCP packets to the single handler that owns each message."""

from future import annotations

from abc import ABC, abstractmethod
from functools import reduce
from typing import List, Optional, Type


# Inbound packet; message is the payload, response is what handlers write.
class TcpPacket:
    """Carry one inbound message and the response written by the chain."""

    def init(self, message: str) -> None:
        self.message = message
        self.response: Optional[str] = None


# Base link; owns successor storage and forwarding mechanics for routing.
# A handler either owns the packet and answers it, or forwards downstream.
class PacketHandler(ABC):
    """Consume a packet or forward it to the successor."""

    def init(self) -> None:
        self._successor: Optional["PacketHandler"] = None

    def set_successor(self, successor: Optional["PacketHandler"]) -> None:
        self._successor = successor

    def _call_next(self, packet: TcpPacket) -> None:
        if self._successor is not None:
            self._successor.handle(packet)

    @abstractmethod
    def handle(self, packet: TcpPacket) -> None:
        raise NotImplementedError


# Keep-alive responder; owns heartbeats before any authentication.
class HeartbeatHandler(PacketHandler):
    """Answer heartbeat packets with ACK and forward everything else."""

    def handle(self, packet: TcpPacket) -> None:
        if packet.message == "HEART_BEAT":
            packet.response = "ACK"
            return
        self._call_next(packet)


# Authentication gate; owns handshakes and guards all business packets.
# Holds session state, so handler order in the builder is security-critical.
class HandshakeHandler(PacketHandler):
    """Authenticate on handshake; reject unauthenticated business packets."""

    def init(self) -> None:
        super().init()
        self._is_authenticated = False

    def handle(self, packet: TcpPacket) -> None:
        if packet.message == "HAND_SHAKE":
            self._is_authenticated = True
            packet.response = "SUCCESS"
            return
        if self._is_authenticated:
            self._call_next(packet)
        else:
            packet.response = "UNAUTHORIZED_ACCESS"


# Receipt printer; owns print commands after authentication.
class PrintHandler(PacketHandler):
    """Consume print packets and forward everything else."""

    def handle(self, packet: TcpPacket) -> None:
        if packet.message == "PRINT":
            packet.response = "SUCCESS"
            return
        self._call_next(packet)


# Payment processor; owns purchase transactions after authentication.
class PurchaseHandler(PacketHandler):
    """Consume purchase packets and forward everything else."""

    def handle(self, packet: TcpPacket) -> None:
        if packet.message == "PURCHASE":
            packet.response = "SUCCESS"
            return
        self._call_next(packet)


# Terminal link; answers unrecognized packets instead of silent drops.
class UnknownPacketHandler(PacketHandler):
    """Fall back to UNKNOWN_MESSAGE as the explicit default response."""

    def set_successor(self, successor: Optional["PacketHandler"]) -> None:
        del successor  # chain ends here by design

    def handle(self, packet: TcpPacket) -> None:
        packet.response = "UNKNOWN_MESSAGE"


# Fluent assembler; links routing handlers and appends the terminator.
# One instance assembles one chain; handlers are mutated during build.
class PosChainBuilder:
    """Accumulate handlers, wire them, append the terminal handler."""

    def init(self) -> None:
        self._handlers: List[PacketHandler] = []

    def with_handler(self, handler: PacketHandler) -> "PosChainBuilder":
        self._handlers.append(handler)
        return self

    def with_handler_type(self, handler_type: Type[PacketHandler]) -> "PosChainBuilder":
        return self.with_handler(handler_type())

    def build(self) -> PacketHandler:
        if not self._handlers:
            raise ValueError("cannot build a chain with no handlers")


def link(left: PacketHandler, right: PacketHandler) -> PacketHandler:
            left.set_successor(right)
            return right

        reduce(link, self._handlers)
        self._handlers[-1].set_successor(UnknownPacketHandler())
        return self._handlers[0]


if name == "main":
    chain = (
        PosChainBuilder()
        .with_handler_type(HeartbeatHandler)
        .with_handler_type(HandshakeHandler)
        .with_handler_type(PrintHandler)
        .with_handler_type(PurchaseHandler)
        .build()
    )

    for msg in ["HEART_BEAT", "PRINT", "HAND_SHAKE", "PRINT", "GARBAGE"]:
        pkt = TcpPacket(msg)
        chain.handle(pkt)
        print(f"{msg:12} -> {pkt.response}")
