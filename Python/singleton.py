from abc import ABCMeta


class MetaSingletonPattern(type):
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super().__call__(*args, **kwargs)
        return cls._instance[cls]


class MetaSingletonABCPattern(ABCMeta):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingletonABCPattern, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# How to use:

class FolanFolan(metaclass=MetaSingletonPattern):
    pass
f_1 = FolanFolan()
f_2 = FolanFolan()
print(f_1 == f_2) #True


class AbstractBlahBlah(metaclass=MetaSingletonABCPattern):
    pass
class BlahBlah(AbstractBlahBlah):
    pass
b_1 = BlahBlah()
b_2 = BlahBlah()
print(b_1 == b_2) #True


class A:
    pass
a_1 = A()
a_2 = A()
print(a_1 == a_2) #False
