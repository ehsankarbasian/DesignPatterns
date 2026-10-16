import copy
from typing import Dict, Optional


'''
You can override python copy.copy() and copy.deepcopy() functions
Just override __copy__ and __deepcopy__ methods inside your class

code from: https://refactoring.guru/design-patterns/prototype/python/example
'''


class SelfReferencingEntity:

    def __init__(self) -> None:
        self.parent: Optional["SomeComponent"] = None

    def set_parent(self, parent: "SomeComponent") -> None:
        self.parent = parent


class SomeComponent:

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
        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        new_object = self.__class__(self.some_int, some_list_of_objects, some_circular_ref)
        new_object.__dict__.update(self.__dict__)
        new_object.some_list_of_objects = some_list_of_objects
        new_object.some_circular_ref = some_circular_ref

        return new_object


    def __deepcopy__(self, memo: Optional[Dict[int, object]] = None) -> "SomeComponent":
        # TODO: When internet is connected completely
        # repair 'mutable default' anti-pattern in refactoring-guru original repository
        # Do not commit it before doing that
        # TODO: Add the pythonic_prototype_hint.md text to comments in the original repository
        if memo is None:
            memo = {}

        """
        Memo is the dictionary that is used by the `deepcopy` library to
        prevent infinite recursive copies in instances of circular references.

        Pass it to all the `copy.deepcopy` calls in the `__deepcopy__`
        implementation to prevent infinite recursions.
        """

        existing = memo.get(id(self))
        if existing is not None:
            return existing  # type: ignore[return-value]

        new_object = self.__class__.__new__(self.__class__)
        memo[id(self)] = new_object

        new_object.some_int = copy.deepcopy(self.some_int, memo)
        new_object.some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        new_object.some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        return new_object
