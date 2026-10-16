"""
Python copy protocol bypasses __init__ during object replication.
Standard deepcopy allocates objects via __new__ and deserializes state,
preventing redundant execution of expensive initialization logic while
requiring dedicated post-clone state reset routines.

Gang of Four Prototype pattern formalizes this state reconfiguration through
an explicit Initialize operation, allowing clients to rebind identity,
reset volatile lifecycle states, and reconfigure parameters on fresh clones
without re-triggering heavy construction workflows.
"""

from __future__ import annotations
import copy
import time
import uuid
from typing import Dict, Optional


# Expensive database service prototype
# Prototype participant enabling constructor bypass and explicit initialization
class DatabaseService:
    """
    Encapsulates persistent connection pooling and expensive schema resolution.

    Trade-offs:
        Bypassing constructor preserves parsed query metadata and schema caches,
        but shifts responsibility to caller to rebind session identity and handles.
    """

    def __init__(self, endpoint: str, pool_capacity: int = 10) -> None:
        print(f"Executing __init__ for endpoint: {endpoint}")
        self.endpoint: str = endpoint
        self.pool_capacity: int = pool_capacity
        self.schema_registry: Dict[str, str] = {
            "accounts": "id, balance, status",
            "transactions": "id, account_id, amount, timestamp",
        }
        self.session_id: str = str(uuid.uuid4())
        self.created_at: float = time.time()
        self.is_connected: bool = True

    def initialize(self, target_endpoint: Optional[str] = None) -> DatabaseService:
        """
        Apply post-clone initialization to reset identity and ephemeral state.
        """

        self.session_id = str(uuid.uuid4())
        self.created_at = time.time()
        self.is_connected = False
        if target_endpoint is not None:
            self.endpoint = target_endpoint
        return self

    def clone(self, target_endpoint: Optional[str] = None) -> DatabaseService:
        """
        Produce deep clone bypassing __init__ and execute initialize protocol.
        """

        cloned_instance = copy.deepcopy(self)
        return cloned_instance.initialize(target_endpoint)

    def status(self) -> str:
        """
        Produce diagnostic summary of current connection state.
        """

        return (
            f"DatabaseService(endpoint={self.endpoint}, "
            f"session_id={self.session_id[:8]}..., "
            f"is_connected={self.is_connected}, "
            f"schema_count={len(self.schema_registry)})"
        )


if __name__ == "__main__":
    print("Instantiating primary prototype via standard constructor invocation:")
    primary_service = DatabaseService(endpoint="primary-cluster.internal:5432")
    print(primary_service.status())

    print("Verifying constructor bypass through standard copy.deepcopy:")
    uninitialized_clone = copy.deepcopy(primary_service)
    print(uninitialized_clone.status())
    is_session_shared = (
        uninitialized_clone.session_id == primary_service.session_id
    )
    print(f"Session identifier shared between original and raw clone: {is_session_shared}")

    print("Applying Prototype clone equipped with explicit Initialize operation:")
    configured_clone = primary_service.clone(
        target_endpoint="secondary-cluster.internal:5432"
    )
    print(configured_clone.status())
    is_session_distinct = (
        configured_clone.session_id != primary_service.session_id
    )
    print(f"Configured clone allocated distinct session identifier: {is_session_distinct}")
    is_schema_preserved = (
        configured_clone.schema_registry == primary_service.schema_registry
    )
    print(f"Configured clone retained precomputed schema registry: {is_schema_preserved}")
