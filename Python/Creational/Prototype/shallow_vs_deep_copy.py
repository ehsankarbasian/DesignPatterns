"""
Demonstrate memory layout differences between shallow copy and deep copy operations.
Explain reference sharing, nested object isolation, and the side effects of mutation.

Trade-offs
    Shallow copies are fast and memory-efficient because they only duplicate outer
    containers while retaining inner references. However, unexpected mutations to
    nested objects will affect all shallow copies sharing those references. Deep copies
    guarantee total isolation of the entire object graph, preventing unintended side
    effects at the expense of higher traversal overhead and memory consumption.
"""

import copy


class InnerAttr:
    """
    Represent leaf object in deeply nested composition hierarchy.
    Leaf node providing isolated state.
    """

    pass


class Attr:
    """
    Represent intermediate composite node holding a reference to inner attribute.
    Intermediate container holding nested reference.
    """

    def __init__(self, inner_attr):
        self.inner_attr = inner_attr


class Obj:
    """
    Represent root composite object holding a reference to intermediate attribute.
    Root container holding reference hierarchy.
    """

    def __init__(self, attr):
        self.attr = attr


# Class example: Object hierarchy memory identity verification

inner_attr = InnerAttr()
attr = Attr(inner_attr=inner_attr)
obj = Obj(attr=attr)

# Shallow copy: Top-level instance is cloned, but nested references remain shared
old_obj_id = id(obj)
obj_copy = copy.copy(obj)
new_obj_id = id(obj_copy)
print(old_obj_id != new_obj_id)

old_attr_id = id(obj.attr)
obj_copy = copy.copy(obj)
new_attr_id = id(obj_copy.attr)
print(old_attr_id == new_attr_id)

old_inner_attr_id = id(obj.attr.inner_attr)
obj_copy = copy.copy(obj)
new_inner_attr_id = id(obj_copy.attr.inner_attr)
print(old_inner_attr_id == new_inner_attr_id)

# Deep copy: Entire object graph is recursively duplicated, creating distinct identities
old_obj_id = id(obj)
obj_copy = copy.deepcopy(obj)
new_obj_id = id(obj_copy)
print(old_obj_id != new_obj_id)

old_attr_id = id(obj.attr)
obj_copy = copy.deepcopy(obj)
new_attr_id = id(obj_copy.attr)
print(old_attr_id != new_attr_id)

old_inner_attr_id = id(obj.attr.inner_attr)
obj_copy = copy.deepcopy(obj)
new_inner_attr_id = id(obj_copy.attr.inner_attr)
print(old_inner_attr_id != new_inner_attr_id)


# List example: Mutation impact on shared vs isolated nested structures

# Shallow copy list: Modifying top-level element is isolated, modifying nested list is shared
my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = my_list.copy()
my_list[3] = 9
my_list[1][1] = 2
print(my_list)  # output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)  # output: [[1, 2, 3], [4, 2, 6], 7, 8]

# Deep copy list: Modifying any level remains completely isolated
my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = copy.deepcopy(my_list)
my_list[3] = 9
my_list[1][1] = 2
print(my_list)  # output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)  # output: [[1, 2, 3], [4, 5, 6], 7, 8] (without any changes)
