from abc import ABCMeta


# How to use:
# class BlahBlah(metaclass=SingletonPattern)
# class AbstractBlahBlah(metaclass=SingletonABCPattern)


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
