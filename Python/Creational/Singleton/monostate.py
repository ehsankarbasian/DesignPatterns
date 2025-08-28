# Also known as Borg pattern
# Different instances but states are the same


print('\nExample 1:')
class Book:
    _shared_state = {"1":"2"}
    
    def __init__(self):
        self.x = 150
        self.__dict__ = self._shared_state


a1 = Book()
a2 = Book()
a1.x = 250

print("book obj 'a1': ", a1)
print("book obj 'a2': ", a2)
print("obj state 'a1': ", a1.__dict__)
print("obj state 'a2': ", a2.__dict__)


# Better example (and better implementation)
print('\nExample 2:')
class Book():
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj


a1 = Book()
a2 = Book()
a3 = Book()
a1.x = "200"
a1.y = "rangi"
a2.x = "300"
a3.z = "20"

print("book obj 'a1': ", a1)
print("book obj 'a2': ", a2)
print("book obj 'a3': ", a3)
print("obj state 'a1': ", a1.__dict__)
print("obj state 'a2': ", a2.__dict__)
print("obj state 'a3': ", a3.__dict__)
