"""
Architecture for expression tree traversal and heterogeneous operations.

Design goal:
Establish a clear separation between structural traversal (Iterator) and
type-specific business operations (Visitor) across an arithmetic expression
composite hierarchy, avoiding fat node interfaces and scattered operation logic.

Key decisions:
- Delegate element navigation to dedicated tree iterators to isolate queue and
  stack traversal mechanics from semantic processing.
- Employ the Visitor pattern with double dispatch to encapsulate multiple
  disparate algorithms (such as decimal evaluation, parenthesized formatting,
  and algebraic constant folding) outside the composite nodes.
- Retain lightweight composite components focused purely on syntax structure
  rather than embedding numerous domain-specific reduction methods.

Trade-offs:
- Simplifies adding new analytical and transformation passes without modifying
  the AST hierarchy.
- Increases system fragility when introducing new expression node variants, as
  all concrete visitors must be updated to satisfy the expanded visitor interface.
"""
