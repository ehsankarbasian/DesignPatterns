# Prototype and Constructors (Python Note)

In classical OOP languages (e.g., Java/C++), cloning is often implemented using copy constructors.

Therefore constructors must be designed to support cloning across the inheritance hierarchy.

In Python this requirement largely disappears because cloning is handled by the **copy protocol** (`copy.copy`, `copy.deepcopy`) rather than constructors.

Instead of defining multiple constructors for cloning, Python classes typically implement:

- `__copy__`
- `__deepcopy__`

Object allocation is performed via `__new__`, and initialization via `__init__` is usually bypassed during cloning.

As a result, constructor design rarely plays a role in implementing the Prototype pattern in Python.
