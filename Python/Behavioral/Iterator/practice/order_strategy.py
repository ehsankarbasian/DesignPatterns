from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from binary_tree import Node


def pre_order(node: Node, sorted_collection: list[Node] = []):
    if node is None:
        return
    
    sorted_collection.append(node)
    pre_order(node.left_child, sorted_collection)
    pre_order(node.right_child, sorted_collection)
    
    return sorted_collection


def post_order(node: Node, sorted_collection: list[Node] = []):
    if node is None:
        return
    
    post_order(node.left_child, sorted_collection)
    post_order(node.right_child, sorted_collection)
    sorted_collection.append(node)
    
    return sorted_collection


def in_order(node: Node, sorted_collection: list[Node] = []):
    if node is None:
        return
    
    in_order(node.left_child, sorted_collection)
    sorted_collection.append(node)
    in_order(node.right_child, sorted_collection)
    
    return sorted_collection
