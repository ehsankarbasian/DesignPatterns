"""
Design goal:
    Demonstrate client interaction with strategy-driven lazy tree traversal and reverse iteration.

Key decisions:
    Construct sample hierarchical binary tree structure.
    Dynamically switch concrete traversal strategies and iterate using standard iteration protocol and reverse iterator.

Trade-offs:
    Direct strategy reassignment on the collection mutates traversal state for subsequent iteration loops.
"""

from binary_tree import BinaryTree
from order_strategy import in_order, post_order, pre_order


# Client
if __name__ == "__main__":
    collection = BinaryTree()
    root = collection.root

    a = collection.add_left_child("a", root)
    b = collection.add_right_child("b", root)
    c = collection.add_left_child("c", a)
    collection.add_left_child("d", c)
    collection.add_right_child("e", c)
    collection.add_right_child("f", a)
    g = collection.add_left_child("g", b)
    collection.add_right_child("h", g)

    collection.iterate_strategy = pre_order
    print("\nPreOrder:")
    for node in collection:
        print(node, end=", ")
    print("\nReverse PreOrder:")
    for node in collection.get_reverse_iterator():
        print(node, end=", ")
    print("\n")

    collection.iterate_strategy = post_order
    print("PostOrder:")
    for node in collection:
        print(node, end=", ")
    print("\nReverse PostOrder:")
    for node in collection.get_reverse_iterator():
        print(node, end=", ")
    print("\n")

    collection.iterate_strategy = in_order
    print("InOrder:")
    for node in collection:
        print(node, end=", ")
    print("\nReverse InOrder:")
    for node in collection.get_reverse_iterator():
        print(node, end=", ")
    print("\n")
