from functools import wraps


def _log_method_call(instance, method):
    method_name = method.__name__
    if not method_name.startswith('_'):
        class_name = str(instance).split()[0].split('.')[-1].replace('<', '')[1:]
        print(f'method "{method_name}" is called on an instance of "{class_name}"')

def _log_property_call(instance, property_name):
    if not property_name.startswith('_'):
        class_name = str(instance).split()[0].split('.')[-1].replace('<', '')[1:]
        print(f'peroperty "{property_name}" is called on an instance of "{class_name}"')


class LogMethodCallsMixin:
    
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr):
            _log_method_call(self, attr)
        else:
            _log_property_call(self, name)
        return attr
