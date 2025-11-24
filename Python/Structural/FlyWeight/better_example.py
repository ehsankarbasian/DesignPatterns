from typing import List


class TreeType:
    
    _name: str
    _color: str
    _texture: str
    
    def __init__(self, name: str, color: str, texture: str):
        self._name = name
        self._color = color
        self._texture = texture
    
    def draw(self, canvas, x, y):
        print(f'Drawing the tree on [{x}, {y}]')


class TreeFactory:
    
    _tree_types: dict = {}
    
    @staticmethod
    def get_tree_type(name: str, color: str, texture: str):
        key = f'{name}-{color}-{texture}'
        type_ = TreeFactory._tree_types.get(key, None)
        
        if type_ is None:
            print(f'Creating new tree: {key}')
            type_ = TreeType(name, color, texture)
            TreeFactory._tree_types[key] = type_
        
        return type_


class Tree:
    
    _x: int
    _y: int
    _type_: TreeType
    
    def __init__(self, x, y, type_):
        self._x = x
        self._y = y
        self._type_ = type_
    
    def draw(self, canvas):
        self._type_.draw(canvas, self._x, self._y)


class Forest:
    
    trees: List[Tree] = []
    
    def plant_tree(self, x, y, name, color, texture):
        type_ = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, type_)
        self.trees.append(tree)
    
    def draw(self, canvas):
        for tree in self.trees:
            tree.draw(canvas)


if __name__ == '__main__':
    forest = Forest()
    
    forest.plant_tree(2, 5, 'siib', 'red', 'wood')
    forest.plant_tree(2, 5, 'siib', 'red', 'wood')
    forest.plant_tree(4, 7, 'potato', 'yellow', 'food')
    forest.plant_tree(3, 2, 'potato', 'yellow', 'food')
    forest.plant_tree(1, 1, 'tomato', 'red', 'wood')
    forest.plant_tree(3, 8, 'siib', 'red', 'wood')
    
    forest.draw(canvas='foo')
