import math

from functools import cached_property


# Semi dynamic solution
# Clear cache in setter methods
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radious(self):
        return self._radius
    
    @radious.setter
    def radious(self, value):
        self._radius = value
        # Clear cache
        if 'area' in self.__dict__:
            del self.__dict__['area']
    
    @cached_property
    def area(self):
        print('Calculating the @cached_property ...')
        return math.pi * self._radius ** 2


c = Circle(radius=5)
print(c.area)
print(c.area)
c.radious = 4
print(c.area)
print(c.area)
