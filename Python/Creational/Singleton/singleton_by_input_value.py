
class MetaSingletonMonoStateByLogfilePattern(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        '''
        class instance key is not only the class
        It's combined with kwargs['log_file]
        So the class is not completely singleton
        It's singleton by kwargs['log_file] value
        If kwargs['log_file] be different, new instance will be created
        '''
        
        log_file = kwargs.get('log_file', '__DEFAULT__')
        cls_key = f'{cls} {log_file}'
        if cls_key not in cls._instance:
            cls._instance[cls_key] = super().__call__(*args, **kwargs)
        return cls._instance[cls_key]


class Logger(metaclass=MetaSingletonMonoStateByLogfilePattern):
    
    # Force the developer to pass log_file as kwargs
    def __init__(self, log_file='sys'):
        '''
        Take the value(s) in the constructor before instantiotion
        Not in the setter method(s) after instantiation
        
        Take it(them) before creating an instance to be able to detect
        whether create a new instance or return a pre-created instance
        
        Force the client developer to pass the value(s) in kwargs
        '''
        
        pass
