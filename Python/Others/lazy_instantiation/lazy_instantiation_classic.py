import math


class Circle:
    def __init__(self, radius):
        self._radius = radius
        self._area = None

    @property
    def area(self):
        print()
        if self._area is None:
            '''
            Do the expensive operations here
            
            Example: Database heavy queries
                     or create a big graph which takes lots of time
                     or even both
            '''
            print("Calculating area...")
            self._area = math.pi * self._radius ** 2
        else:
            print("Area has been calculated bfore !")
        return self._area


c = Circle(radius=5)
print(c.area)
print(c.area)
print(c.area)
