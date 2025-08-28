import math

from functools import cached_property


'''
Dynamic solution:
    Modify the decorator @cached_property
'''


class _InputTypeException(Exception):
    pass


class DependentCachedProperty(cached_property):
    def __init__(self, func, depends_on):
        # TODO: Validate that the owner class inherits from CachedPropertyDependencyMixin
        
        # Validate that depends_on is a list
        if not type(depends_on) is list:
            raise _InputTypeException('depends_on Must be a list')
        self.depends_on = depends_on
        
        super().__init__(func)


def dependent_cached_property(depends_on):
    def wrapper(func):
        return DependentCachedProperty(func, depends_on)
    return wrapper


class CachedPropertyDependencyMixin:
    
    def __setattr__(self, attr_name, value):
        super().__setattr__(attr_name, value)

        # Invalidate all dependent cached_propertis
        for key, attr_value in type(self).__dict__.items():
            is_dependent_property = isinstance(attr_value, DependentCachedProperty)
            
            if is_dependent_property:
                is_depended = attr_name in attr_value.depends_on
                
                if is_depended:
                    if key in self.__dict__:
                        self.__dict__.pop(key, None)
    
    
    def invalidate_cache(self, *names):
        # Invalidate cached propeties manually
        for attr_name in names:
            if attr_name not in type(self).__dict__:
                raise Exception(f'AttibuteError: {self.__class__} has no attribute: "{attr_name}"')
            attr_value = type(self).__dict__[attr_name]
            if isinstance(attr_value, DependentCachedProperty) or isinstance(attr_value, cached_property):
                self.__dict__.pop(attr_name, None)


class Circle(CachedPropertyDependencyMixin):
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radious(self):
        return self._radius
    
    @radious.setter
    def radious(self, value):
        self._radius = value
    
    @dependent_cached_property(depends_on=['radious'])
    def area(self):
        print('Calculating the @cached_property ...')
        return math.pi * self._radius ** 2


c = Circle(radius=5)
print(c.area)
print(c.area)
c.radious = 4
print('radious changed')
print(c.area)
print(c.area)
c.invalidate_cache('area')
print('area cache invalidated')
print(c.area)
print(c.area)
