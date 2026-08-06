from __future__ import annotations

from abc import ABC, abstractmethod
import zlib


# Interface
class DataSourceInterface(ABC):

    @abstractmethod
    def write_data(self, data: bytes) -> None:
        pass

    @abstractmethod
    def read_data(self) -> bytes:
        pass


# Component
class MemoryDataSource(DataSourceInterface):

    def __init__(self) -> None:
        self._data = b""

    def write_data(self, data: bytes) -> None:
        self._data = data

    def read_data(self) -> bytes:
        return self._data


# Base Decorator
class DataSourceDecorator(DataSourceInterface):

    def __init__(self, source: DataSourceInterface) -> None:
        self._wrappee = source  # Wrappee

    def write_data(self, data: bytes) -> None:
        self._wrappee.write_data(data)

    def read_data(self) -> bytes:
        return self._wrappee.read_data()


# Decorator
class EncryptionDecorator(DataSourceDecorator):

    def __init__(self, source: DataSourceInterface, key: bytes) -> None:
        super().__init__(source)
        self._key = key

    def write_data(self, data: bytes) -> None:
        encrypted = self._xor(data)
        super().write_data(encrypted)

    def read_data(self) -> bytes:
        encrypted = super().read_data()
        return self._xor(encrypted)

    def _xor(self, data: bytes) -> bytes:
        return bytes(
            byte ^ self._key[index % len(self._key)]
            for index, byte in enumerate(data)
        )


# Decorator
class CompressionDecorator(DataSourceDecorator):

    def write_data(self, data: bytes) -> None:
        compressed = zlib.compress(data)
        super().write_data(compressed)

    def read_data(self) -> bytes:
        compressed = super().read_data()
        return zlib.decompress(compressed)


if __name__ == "__main__":
    
    source: DataSourceInterface
    
    source = EncryptionDecorator(       # Wrapper
        CompressionDecorator(           # Wrapper
            MemoryDataSource()          # Component
        ),
        key=b"key"
    )

    source.write_data(b"hello")

    print(source.read_data())
