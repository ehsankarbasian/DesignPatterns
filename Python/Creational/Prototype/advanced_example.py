import copy


'''
You can override python copy.copy() and copy.deepcopy() functions
Just override __copy__ and __deepcopy__ methods inside your class

code from: https://refactoring.guru/design-patterns/prototype/python/example
'''


class SelfReferencingEntity:
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class SomeComponent:

    def __init__(self, some_int, some_list_of_objects, some_circular_ref):
        self.some_int = some_int
        self.some_list_of_objects = some_list_of_objects
        self.some_circular_ref = some_circular_ref

    def __copy__(self):
        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        new_object = self.__class__(self.some_int, some_list_of_objects, some_circular_ref)
        new_object.__dict__.update(self.__dict__)

        return new_object

    def __deepcopy__(self, memo={}):
        """
        Memo is the dictionary that is used by the `deepcopy` library to
        prevent infinite recursive copies in instances of circular references.
        
        Pass it to all the `copy.deepcopy` calls in the `__deepcopy__`
        implementation to prevent infinite recursions.
        """

        some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        new_object = self.__class__(self.some_int, some_list_of_objects, some_circular_ref)
        new_object.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new_object


if __name__ == "__main__":

    list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, list_of_objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)

    # Change the list in shallow_copied_component
    shallow_copied_component.some_list_of_objects.append("another object")
    assert shallow_copied_component.some_list_of_objects[-1] == "another object"
    assert component.some_list_of_objects[-1] == "another object"
    # It changes in component too

    # Change the set in the list of objects.
    component.some_list_of_objects[1].add(4)
    assert 4 in component.some_list_of_objects[1]
    assert 4 in shallow_copied_component.some_list_of_objects[1]
    # It changes in shallow_copied_component too

    deep_copied_component = copy.deepcopy(component)

    # Change the list in deep_copied_component
    deep_copied_component.some_list_of_objects.append("one more object")
    assert deep_copied_component.some_list_of_objects[-1] == "one more object"
    assert component.some_list_of_objects[-1] != "one more object"
    # Not changed the component

    # Change the set in the list of objects.
    component.some_list_of_objects[1].add(10)
    assert 10 in component.some_list_of_objects[1]
    assert 10 not in deep_copied_component.some_list_of_objects[1]
    # Not changed deep_copied_component

    id_1 = id(deep_copied_component.some_circular_ref.parent)
    id_2 = id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent)
    assert id_1 == id_2
    # Deepcopied objects contain same reference
    # hey are not cloned repeatedly."
