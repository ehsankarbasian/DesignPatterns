"""
Educational Prototype example demonstrating custom copy protocols in Python.

Design goal:
    Showcase how objects customize duplication semantics by implementing
    __copy__ and __deepcopy__ dunder methods, enabling explicit control
    over member aliasing, instance allocation, and recursive cycle resolution.

Key decisions:
    __copy__ creates a shallow replica by sharing nested mutable objects
    while instantiating a distinct container.
    __deepcopy__ allocates uninitialized instances via __new__ and immediately
    populates the memo dictionary with the object identity before deep-copying
    fields, breaking circular reference loops.

Trade-offs
    Custom protocol methods grant granular control over graph reconstruction,
    yet increase maintenance burden as changes to internal fields require
    synchronizing copy routines.
"""

import copy
from typing import Dict, Optional


class SelfReferencingEntity:
    """
    Component collaborator establishing cyclical object references.
    Collaborator role modeling back-references in interconnected domain graphs.

    Trade-offs
        Introducing cyclic references requires rigorous memoization during deep
        traversal, risking infinite recursion if memo dictionaries are dropped.
    """

    def __init__(self) -> None:
        self.parent: Optional["SomeComponent"] = None

    def set_parent(self, parent: "SomeComponent") -> None:
        """
        Bind the back-reference pointer to the owning component.
        """
        
        self.parent = parent


class SomeComponent:
    """
    Compound prototype implementing customized copy dunder protocols.
    Prototype role demonstrating shallow versus deep attribute replication.

    Trade-offs
        Bypassing standard copy automation via manual dunder implementations
        ensures cycle resilience, but introduces boilerplate attribute wiring.
    """

    def __init__(
        self,
        some_int: int,
        some_list_of_objects: list[object],
        some_circular_ref: SelfReferencingEntity,
    ) -> None:
        self.some_int = some_int
        self.some_list_of_objects = some_list_of_objects
        self.some_circular_ref = some_circular_ref


    def __copy__(self) -> "SomeComponent":
        """
        Produce a shallow copy with duplicated containers and shared references.
        """

        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        new_object = self.__class__(self.some_int, some_list_of_objects, some_circular_ref)
        new_object.__dict__.update(self.__dict__)
        new_object.some_list_of_objects = some_list_of_objects
        new_object.some_circular_ref = some_circular_ref

        return new_object


    def __deepcopy__(self, memo: Optional[Dict[int, object]] = None) -> "SomeComponent":
        """
        Produce a deep copy while utilizing a memo mapping to resolve reference cycles.
        Allocates instance via __new__ to register identity before nested traversal.
        """

        if memo is None:
            memo = {}

        existing = memo.get(id(self))
        if existing is not None:
            return existing  # type: ignore[return-value]

        new_object = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_object

        new_object.some_int = copy.deepcopy(self.some_int, memo)
        new_object.some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        new_object.some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        return new_object


if __name__ == "__main__":
    list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, list_of_objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)
    shallow_copied_component.some_list_of_objects.append("another object")
    if component.some_list_of_objects[-1] == "another object":
        print(
            "Adding elements to `shallow_copied_component`'s "
            "some_list_of_objects adds it to `component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Adding elements to `shallow_copied_component`'s "
            "some_list_of_objects doesn't add it to `component`'s "
            "some_list_of_objects."
        )

    deep_copied_component = copy.deepcopy(component)
    deep_copied_component.some_list_of_objects.append("one more object")
    if component.some_list_of_objects[-1] == "one more object":
        print(
            "Adding elements to `deep_copied_component`'s "
            "some_list_of_objects adds it to `component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Adding elements to `deep_copied_component`'s "
            "some_list_of_objects doesn't add it to `component`'s "
            "some_list_of_objects."
        )
