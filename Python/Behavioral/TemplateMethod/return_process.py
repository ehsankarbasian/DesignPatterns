"""
TODO

Model an order-return process as an exercise in the Template Method pattern.

The domain centers on returning a customer's order. The shared return workflow
creates a return transaction, calculates the refund, restores eligible items to
stock, and pays the customer. Return policies vary in how much of the order is
accepted and how much money is refunded.

The exercise should distinguish the invariant workflow from policy-specific
steps. A full-return policy accepts all items and refunds the full amount. A
penalty policy accepts all items but refunds only 80 percent of the amount
paid. A partial-quantity policy accepts at most half of the ordered quantity
and refunds the full amount associated with the accepted portion, without an
additional penalty.

When implementing the example, define the meaning of the refund base precisely:
the accepted quantity, product price, and any eligible postage amount must be
handled consistently. Represent monetary values with Decimal and enforce
invariants, including nonnegative refunds and a refund that does not exceed the
eligible amount paid.

The exercise should make clear which operations belong to the fixed return
workflow and which vary by policy. Consider whether creating the return
transaction is a factory method, whether policy-specific calculations are
primitive operations, and whether any optional extension point is genuinely
needed. Avoid adding hooks or abstract operations that do not express a real
variation in the domain.

Trade-offs
    A shared workflow reduces duplication and makes the processing order
    explicit, but inheritance couples each policy to the base algorithm.
    Compare this structure with a strategy-based design if the policies vary
    independently from the workflow or need to be composed.
"""
