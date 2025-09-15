from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import Node
    from iterator import BinaryTreeIterator


def preorder(node: Node, sorted_collection: list[Node] = []):
    if node is None:
        return
    
    sorted_collection.append(node)
    preorder(node.left_child, sorted_collection)
    preorder(node.right_child, sorted_collection)
    
    return sorted_collection
