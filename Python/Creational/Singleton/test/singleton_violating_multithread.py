import time
from abc import ABCMeta
from threading import Lock


class SingletonPatternThreadSafeToViolate(type):
    _instances = {}

    # _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        # with cls._lock:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            value = kwargs.get('value', None)
            if value == 2:
                time.sleep(2)
            cls._instances[cls] = instance
        
        return cls._instances[cls]


class SingletonABCPatternThreadSafeToViolate(ABCMeta):
    _instances = {}
    
    # _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        # with cls._lock:
        if cls not in cls._instances:
            instance = super(SingletonABCPatternThreadSafeToViolate, cls).__call__(*args, **kwargs)
            value = kwargs.get('value', None)
            if value == 2:
                time.sleep(2)
            cls._instances[cls] = instance
        
        return cls._instances[cls]
