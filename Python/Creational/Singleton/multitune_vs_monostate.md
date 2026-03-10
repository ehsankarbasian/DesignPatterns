# Multiton vs Monostate (Borg) — Quick Cheatsheet

| Aspect | Multiton | Monostate (Borg) |
|---|---|---|
| Core Idea | One instance **per key** | Many instances but **shared state** |
| Instance Identity | Same key → same instance | Every instantiation creates a new instance |
| State Sharing | Not required | All instances share the same state (`__dict__`) |
| Instance Count | Multiple (controlled by key) | Unlimited |
| State Location | Inside each instance | Shared dictionary between instances |
| Typical Implementation | Cache instances in a dict keyed by identifier | Assign `self.__dict__` to a shared dict |
| Example Key | `Logger(log_file="app.log")` | Not key‑based |
| Identity Check | `a is b` if keys are equal | `a is b` is False |
| State Check | State may differ between keys | State always identical across instances |
| Use Case | Resource per identifier (loggers, DB connections, caches) | Global configuration/state shared everywhere |
| Pattern Family | Variant of **Singleton** | Alternative to **Singleton** |
| Primary Goal | Controlled instance reuse | Shared mutable state |

## Mental Model

Multiton:

```
key → instance
```

Example:

```
Logger("app.log")   -> instance A
Logger("app.log")   -> instance A
Logger("error.log") -> instance B
```

Monostate (Borg):

```
instance → shared state
```

Example:

```
a = Config()
b = Config()

a is b            # False

a.theme = "dark"
b.theme           # "dark"
```
