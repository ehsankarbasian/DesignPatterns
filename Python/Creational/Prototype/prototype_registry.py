import copy


# Base class (prototype)
class Shape:
    
    def clone(self):
        """
        Return a deep copy of this object.
        Each concrete prototype can override if needed.
        """
        return copy.deepcopy(self)


# Concrete classes
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius


# Prototype registry
class ShapeRegistry:
    # Stores prototype instances and returns clones of them if needed

    def __init__(self):
        self._prototypes = {}

    def register(self, name, shape):
        self._prototypes[name] = shape

    def unregister(self, name):
        del self._prototypes[name]

    def clone(self, name):
        shape = self._prototypes[name]
        return shape.clone()


# Client
if __name__ == '__main__':
    registry = ShapeRegistry()

    registry.register("big_circle", Circle(10))
    registry.register("small_rectangle", Rectangle(2, 4))

    shape1 = registry.clone("big_circle")
    shape2 = registry.clone("big_circle")

    print(id(shape1) != id(shape2))
