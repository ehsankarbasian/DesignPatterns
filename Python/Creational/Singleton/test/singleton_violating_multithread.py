from threading import Lock
import time


class SingletonPatternThreadSafe(type):
    _instances = {}

    # _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        # with cls._lock:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            value = kwargs.get('value', None)
            if value:
                print ('instance {value} created')
            if value == 2:
                print('thread 2 waiting 2 seconds to assingg the instance in cls._instances[cls] ...')
                time.sleep(2)
            cls._instances[cls] = instance
        
        return cls._instances[cls]
