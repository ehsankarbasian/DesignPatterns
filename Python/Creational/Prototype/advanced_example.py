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
