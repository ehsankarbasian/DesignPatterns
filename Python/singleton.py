from abc import ABCMeta


class SingletonPattern(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABCPattern(ABCMeta):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCPattern, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# How to use:

class A:
    pass
a_1 = A()
a_2 = A()
assert(a_1 != a_2)


class FolanFolan(metaclass=SingletonPattern):
    pass
class FolanFolanChild(FolanFolan):
    pass
f_1 = FolanFolan()
f_2 = FolanFolan()
ffc_1 = FolanFolanChild()
ffc_2 = FolanFolanChild()
assert(f_1 == f_2) #True
assert(ffc_1 == ffc_2) #True
assert(f_1 != ffc_1) #False


class AbstractSingletonBlahBlah(metaclass=SingletonABCPattern):
    pass
class BlahBlah(AbstractSingletonBlahBlah):
    pass
class ClahClah(AbstractSingletonBlahBlah):
    pass
b_1 = BlahBlah()
b_2 = BlahBlah()
c_1 = ClahClah()
c_2 = ClahClah()
assert(b_1 == b_2) #True
assert(c_1 == c_2) #True
assert(b_1 != c_1) #False
