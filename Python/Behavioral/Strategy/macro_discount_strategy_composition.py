"""
TODO: Implement a macro discount strategy using Strategy composition (Composite of strategies).

Problem Statement:
Model a discount subsystem where multiple independent discount rules must be applied as a single
strategy, while keeping each rule isolated, reusable, and independently testable.

Domain Requirements:
- Define a composite discount strategy that itself behaves like a discount strategy.
- The composite strategy holds an ordered collection of child strategies and applies them to a basket context.
- Support different composition policies, such as:
  - additive discounts (sum of discounts)
  - sequential discounts (apply rule A then rule B on the reduced base)
  - capped aggregation (never exceed gross amount)
  - priority-based selection (first applicable strategy wins)
- Enforce monetary invariants centrally:
  - final discount must not be negative
  - final discount must not exceed the basket gross amount
- Client code must treat the macro strategy exactly like any other single strategy without inspecting internals.
- Ensure the design stays extensible when new discount rules and new composition policies are added.
"""
