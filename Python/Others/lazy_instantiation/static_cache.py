import math

from functools import cache, cached_property


# Not to cahce
def simple_factorial(n):
    print(f'Call simple_factorial {n}')
    return n * simple_factorial(n-1) if n else 1

print ('\n--------> calling simple_factorial(10)')
print(f'RESULT: {simple_factorial(10)}')      # makes 11 recursive calls
print ('\n--------> calling simple_factorial(5)')
print(f'RESULT: {simple_factorial(5)}')       # makes 6 recursive calls
print ('\n--------> calling simple_factorial(12)')
print(f'RESULT: {simple_factorial(12)}')      # makes 13 recursive calls


@cache
def cached_factorial(n):
    print(f'Call cached_factorial {n}')
    return n * cached_factorial(n-1) if n else 1

print ('\n--------> calling cached_factorial(10)')
print(f'RESULT: {cached_factorial(10)}')      # No cache --> makes 11 recursive calls
print ('\n--------> calling cached_factorial(5)')
print(f'RESULT: {cached_factorial(5)}')       # No calls (read from cache)
print ('\n--------> calling cached_factorial(12)')
print(f'RESULT: {cached_factorial(12)}')      # No caches for 11, 12 --> makes 2 calls


# Using decorator: @property
class Circle:
    def __init__(self, radius):
        self._radius = radius
        self._area = None

    @property
    def area(self):
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


print('\nExample 1')
c = Circle(radius=5)
print(c.area)
print(c.area)
print(c.area)


# The beter way
# Using decorator: @cached_property 
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @cached_property
    def area(self):
        print('Calculating the @cached_property for the first time ...')
        return math.pi * self._radius ** 2


print('\nExample 2')
c = Circle(radius=5)
print(c.area)
print(c.area)

# BUG and the hardcode solution
print('\nBUG of Example 2')
c._radius = 4
print(c.area)
del c.__dict__['area']
print(c.area)
print(c.area)

# The is solved in next files
