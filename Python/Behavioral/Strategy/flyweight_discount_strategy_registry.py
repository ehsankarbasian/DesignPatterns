"""
TODO: Implement a flyweight registry for discount strategies to reduce redundant object creation.

Problem Statement:
In a system with many discount rules, creating a new concrete strategy instance per basket or request
can lead to unnecessary object proliferation. Most discount strategies are stateless or parameterized
by a small configuration and can be shared safely.

Domain Requirements:
- Provide a registry that returns reusable strategy instances by a stable key (string or enum).
- Support two categories of strategies:
  - singleton-like strategies that are fully stateless and shareable
  - parameterized strategies that can be cached by configuration key (e.g., percentage=10)
- Ensure cache keys are explicit and collision-safe (e.g., ("percentage", "10") rather than "10").
- Make the registry the only construction path used by client code for registered strategies.
- Allow pre-registration of commonly used strategies and lazy registration for optional rules.
- Keep the registry focused on lifecycle and reuse, not on business rule selection.
- Preserve type expectations: the registry must only return objects conforming to the discount strategy interface.
"""
