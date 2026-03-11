# Thread Safety Policy (Borg / Shared State)

This policy defines synchronization responsibilities when using Borg‑style shared state.
The goal is to prevent race conditions and ensure consistent access when instances share mutable data.

---

## Case 1 — Borg / Mixin Level Lock

If a Borg implementation shares the entire instance `__dict__`:
<br>**All updates to the shared state must be synchronized at the Borg class level via a central lock.**

Example implementation: `threadsafe_examples/mixin.py`

---

## Case 2 — Attribute-Level Lock

If only specific attributes represent shared mutable state:

- The lock must be colocated with the attribute’s storage (shared binding).
- All reads and writes to that attribute must acquire the lock.
- Direct uncontrolled assignment must be avoided.

Rule:
If an attribute is shared, the lock belongs to that attribute.

Example implementation: `threadsafe_examples/basic.py`

---

## Case 3 — Descriptor-Level Lock

If shared attributes are implemented using descriptors:

- The descriptor is responsible for synchronizing access.
- The lock must be owned by the descriptor instance and used within its `__get__`, `__set__`, and `__delete__` methods.
- The owning class must not bypass the descriptor storage.

Example implementation:
See `threadsafe_examples/descriptor.py`

---

## Enforcement Guideline

If shared state can be modified without acquiring the intended lock, the design is invalid.  
Every modification path must be verifiably synchronized via one of the above mechanisms.
