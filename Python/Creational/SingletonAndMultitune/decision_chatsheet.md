# Singleton in Python - Decision Cheat Sheet

Use this quick guide when you *think* you need a Singleton.

## Prefer This First

**Module-level instance**
- Need one shared object (config, registry, client)?
- Importing a module already gives a single shared instance.

Example:
```
# config.py
config = Config()
```

---

## When Dependency Injection Is Better

- You want **easy unit testing**
- Different implementations may be swapped
- You want to avoid **hidden global state**

Rule of thumb:

> If the object is part of business logic, prefer **Dependency Injection**.

---

## When Real Singleton Makes Sense

Use a real singleton only when:

- There must be **exactly one instance globally**
- Multiple creations could break correctness

Typical cases:
- logger manager
- connection pool manager
- global cache coordinator

---

## Borg / Monostate (Rare but Useful)

Use if:

- Instances can be multiple
- But **state must stay shared**

All objects share the same `__dict__`.

---

## Thread‑Safety Reminder

If objects may be created from multiple threads:

- protect instance creation with a **Lock**
- test using **Barrier** to force race conditions

---

## Quick Decision Rule

```
Need one shared object?
    ↓
Try module instance first
    ↓
Need testability / flexibility?
    ↓
Use dependency injection
    ↓
Hard guarantee of single instance required?
    ↓
Use real Singleton
```