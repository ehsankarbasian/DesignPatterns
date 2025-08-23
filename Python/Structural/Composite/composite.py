from abc import ABC, abstractmethod


class GraphicInterface(ABC):
    
    @abstractmethod
    def move(self, x, y):
        pass
    
    @abstractmethod
    def draw(self):
        pass


class Dot(GraphicInterface):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def draw(self):
        print(f'Drawing Dot ({self.x}, {self.y})')


class Circle(Dot):
    
    def __init__(self, x, y, radius):
        self.radius = radius
        super().__init__(x, y)
    
    def draw(self):
        print(f'Drawing Circle ({self.x}, {self.y}, {self.radius})')


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
        for child in self.__children:
            child.draw()
            # Update the bounding rectangle.
        # Draw a dashed rectangle using the bounding coordinates


class ImageEditor:
    
    def __init__(self):
        self.all = CompoundGraphic()
    
    def add_shape(self, obj):
        self.all.add(obj)
    
    def group_selected(self, components):
        _group = CompoundGraphic()
        
        for component in components:
            _group.add(component)
            self.all.remove(component)
        
        self.all.add(_group)

    
    def _draw_all(self):
        self.all.draw()


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
