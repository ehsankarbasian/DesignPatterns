from binary_tree import BinaryTree
from order_strategy import preorder


collection = BinaryTree()
root = collection.root
a = collection.add_left_child('a', root)
b = collection.add_right_child('b', root)
c = collection.add_left_child('c', a)
d = collection.add_left_child('d', c)
e = collection.add_right_child('e', c)
f = collection.add_right_child('f', a)
g = collection.add_left_child('g', b)
h = collection.add_right_child('h', g)


collection.iterate_strategy = preorder

for c in collection:
    print(c, end=', ')
print()

print()
for c in collection.get_reverse_iterator():
    print(c, end=', ')
print()
