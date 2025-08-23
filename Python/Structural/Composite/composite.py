from abc import ABC, abstractmethod
import sys

_indent_level = 0

def _print_indented(text):
    global _indent_level
    text = _indent_level*'    ' + text
    sys.stdout.write(text+"\n")

print = _print_indented


class GraphicInterface(ABC):
    
    @abstractmethod
    def move(self, x, y):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def __str__(self):
        return f'{self.__class__.__name__} (id:{str(id(self))[-5:]})'


# Leaf
class Dot(GraphicInterface):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def draw(self):
        print(f'Drawing {self} ({self.x}, {self.y})')


# Leaf
class Circle(Dot):
    
    def __init__(self, x, y, radius):
        self.radius = radius
        super().__init__(x, y)
    
    def draw(self):
        print(f'Drawing {self} ({self.x}, {self.y}, {self.radius})')


# NOT Leaf
class CompoundGraphic(GraphicInterface):
    
    def __init__(self):
        self.__children = []
    
    def add(self, child: GraphicInterface):
        self.__children.append(child)
    
    def remove(self, child):
        self.__children.remove(child)
    
    def move(self, x, y):
        for child in self.__children:
            child.move(x, y)
    
    def draw(self):
        global _indent_level
        print(f'--> Begin draw {self}')
        _indent_level += 1
        
        for child in self.__children:
            child.draw()
            # Update the bounding rectangle.
        # Draw a dashed rectangle using the bounding coordinates
        
        _indent_level -= 1
        print(f'--> End draw {self}')


class ImageEditor:
    
    def __init__(self):
        # Composite structure root
        self.root = CompoundGraphic()
    
    def add_shape(self, obj):
        self.root.add(obj)
    
    def group_selected(self, components):
        # Composite structure SubBranch
        # group in neither Leaf nor Root
        _group = CompoundGraphic()
        
        for component in components:
            _group.add(component)
            self.root.remove(component)
        
        self.root.add(_group)
    
    def _draw_all(self):
        self.root.draw()


editor = ImageEditor()

dot_1 = Dot(1, 2)
dot_2 = Dot(3, 5)
circle_1 = Circle(2, 7, 5)
circle_2 = Circle(5, 3, 10)

editor.add_shape(dot_1)
editor.add_shape(dot_2)
editor.add_shape(circle_1)
editor.add_shape(circle_2)

selected = [dot_1, circle_1]
editor.group_selected(selected)
editor._draw_all()
