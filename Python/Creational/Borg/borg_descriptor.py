
# Define SharedAttribute using Descriptor protocol
# Sharing the attribute is handled by the Descriptor
# Setter, Getter & Deleter logic for SharedAttribute will be handled by the descriptor below
class SharedAttribute:
    def __init__(self, initial_value=None):
        self.value = initial_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("value must be >= 0")
        self.value = value

    def __delete__(self, instance):
        raise AttributeError("cannot delete shared attribute")


# How to use
class Borg:
    counter = SharedAttribute(0)

    def __init__(self):
        self.__dict__ = self._shared_state

    _shared_state = {}


# Client code
if __name__ == '__main__':
    a = Borg()
    b = Borg()
    a.counter = 10
    print(b.counter)   # 10
