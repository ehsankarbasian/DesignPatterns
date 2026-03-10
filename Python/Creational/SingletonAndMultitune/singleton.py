from abc import ABCMeta


# How to use:
# class BlahBlah(metaclass=SingletonPattern)
# class AbstractBlahBlah(metaclass=SingletonABCPattern)


class SingletonPattern(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonABCPattern(ABCMeta):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(SingletonABCPattern, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
