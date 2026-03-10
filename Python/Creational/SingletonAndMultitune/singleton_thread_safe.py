from abc import ABCMeta
from threading import Lock


class SingletonPatternThreadSafe(type):
    _instances = {}
    _locks = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._locks:
            cls._locks[cls] = Lock()
        
        with cls._locks[cls]:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        
        return cls._instances[cls]


class SingletonABCPatternThreadSafe(ABCMeta):
    _instances = {}
    _locks = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._locks:
            cls._locks[cls] = Lock()
        
        with cls._locks[cls]:
            if cls not in cls._instances:
                instance = super(SingletonABCPatternThreadSafe, cls).__call__(*args, **kwargs)
                cls._instances[cls] = instance
        
        return cls._instances[cls]
