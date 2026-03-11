
# Borg Pattern Implementations — Comparison

This table compares three implementation strategies used in this repository for Borg-style shared state and thread safety.

| Aspect | Basic (Attribute-Level Lock) | Descriptor-Based | Mixin / Borg-Level Lock |
|---|---|---|---|
| Core Idea | Shared attributes are protected individually with locks located near the attribute storage. | Shared attributes are implemented via descriptors that own their synchronization logic. | Entire instance `__dict__` is shared across instances and protected with a central lock. |
| Lock Location | Near the shared attribute (class-level or shared binding). | Inside the descriptor instance. | Central lock defined in the Borg/mixin class. |
| Synchronization Scope | Per shared attribute. | Per descriptor (per attribute abstraction). | Global shared state (`__dict__`). |
| Selective Shared State | Possible but manual and error‑prone. | Yes — descriptors explicitly define which attributes participate in shared state. | No — the whole state dictionary is shared. |
| Encapsulation of Concurrency Logic | Medium — locking logic may spread across methods. | High — descriptor encapsulates all access control. | Low — global lock often handled outside attribute logic. |
| Risk of Accidental Unsafe Access | Medium — direct attribute access can bypass policy. | Low — descriptor mediates access. | Medium — direct dict mutation can bypass conventions. |
| Implementation Complexity | Low to Medium. | Medium to High. | Low. |
| Maintainability | Moderate — logic can scatter across code. | High — concurrency policy localized in descriptor. | Moderate — simple but coarse-grained. |
| Performance Characteristics | Fine-grained locking; good scalability if attributes are independent. | Fine-grained and explicit; similar to attribute-level but cleaner abstraction. | Coarse-grained locking; can become contention bottleneck. |
| Flexibility | Moderate. | High — descriptors allow reusable shared-state components. | Low — everything shares the same storage model. |
| Best Use Case | Small systems with a few shared attributes. | Systems requiring selective shared state and strong encapsulation. | Simple Borg implementations where full shared state is acceptable. |

---

## Key Takeaways

- **Descriptor-based designs provide the cleanest encapsulation of synchronization logic.**
- **Attribute-level locking works but can lead to scattered concurrency logic.**
- **Mixin/Borg-level locking is the simplest approach but sacrifices selectivity and scalability.**

---

### Note (selective shared attriburtes) :
With descriptors, each attribute can be defined individually, so it is possible to choose which attributes participate in shared state. This makes the design selective.
In the previous two approaches (Borg/Mixin and full shared `__dict__` patterns), the entire instance state is shared, so the shared state is not selective.
