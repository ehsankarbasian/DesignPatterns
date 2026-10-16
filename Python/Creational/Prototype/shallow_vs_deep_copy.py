import copy


# Class example:

class InnerAttr:
            pass
        
class Attr:
    def __init__(self, inner_attr):
        self.inner_attr = inner_attr

class Obj:
    def __init__(self, attr):
        self.attr = attr


inner_attr = InnerAttr()
attr = Attr(inner_attr = inner_attr)
obj = Obj(attr=attr)


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



# List example:

my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = my_list.copy()
my_list[3] = 9
my_list[1][1] = 2
print(my_list)    #output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)   #output: [[1, 2, 3], [4, 2, 6], 7, 8]


my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = copy.deepcopy(my_list)
my_list[3] = 9
my_list[1][1] = 2
print(my_list)    #output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)   #output: [[1, 2, 3], [4, 5, 6], 7, 8] (without any changes)
