from __future__ import annotations

from iterator import AbstractBaseIterable


class Node:
    
    def __init__(self,
                 node_name: str,
                 parent: GraphConnection = None):
        self._name = node_name
        self._parent: GraphConnection = parent
        
        self._left_child: GraphConnection = None
        self._right_child: GraphConnection = None
    
    @property
    def parent(self) -> Node:
        return self._parent
    
    @property
    def left_child(self) -> Node:
        return self._left_child
    
    @property
    def right_child(self) -> Node:
        return self._right_child
    
    def _add_left_child(self, left_child: Node):
        if self._left_child:
            raise Exception('Has left child')
        self._left_child = left_child
    
    def _add_right_child(self, right_child: Node):
        if self._right_child:
            raise Exception('Has right child')
        self._right_child = right_child
    
    def __str__(self):
        return self._name


GraphConnection = Node | None

class BinaryTree(AbstractBaseIterable):
    
    @property
    def iterate_strategy(self):
        return self._iterate_strategy
    
    @iterate_strategy.setter
    def iterate_strategy(self, value: function):
        self._iterate_strategy = value
    
    def __init__(self):
        root = Node(node_name='root')
        self._collection: list[Node] = [root]
    
    @property
    def root(self) -> Node:
        return self._collection[0]
    
    def add_left_child(self, name: str, parent: Node) -> Node:
        child = Node(name, parent)
        parent._add_left_child(child)
        self._collection.append(child)
        return child
    
    def add_right_child(self, name: str, parent: Node) -> Node:
        child = Node(name, parent)
        parent._add_right_child(child)
        self._collection.append(child)
        return child
