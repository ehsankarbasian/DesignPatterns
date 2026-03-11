# Shared Thread-Safe Configuration (Borg-style Example)

## Goal
A small educational example showing how a **shared configuration object** can be implemented using a Borg-style shared state combined with **thread-safe descriptors**.

The project focuses on the idea of **shared state across instances** while keeping writes safe in multi-threaded scenarios.

## Files
- `descriptors.py` – contains `SharedField`, a thread-safe descriptor that stores shared values.
- `config.py` – defines the `Config` class that uses `SharedField` for shared configuration fields.
- `how_to_use.py` – simple demonstration script showing typical usage and behavior.
- `test_config.py` – unit tests verifying shared state and thread-safety behavior.

## Suggested Reading Order
1. `descriptors.py`
2. `config.py`
3. `how_to_use.py`
4. `test_config.py`

Start from the descriptor implementation, then see how it is used in the configuration class, and finally review the usage example and tests.
