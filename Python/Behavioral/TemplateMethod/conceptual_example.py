from abc import ABC, abstractmethod


# Code from: https://refactoring.guru/design-patterns/template-method/python/example

class AbstractClass(ABC):

    def template_method(self):
        # The skeleton of an algorithm.

        self.base_operation_1()
        self.required_operations_1()
        self.base_operation_2()
        self.hook_1()
        self.required_operations_2()
        self.base_operation_3()
        self.hook_2()

    # These operations already have implementations.
    def base_operation_1(self):
        print("AbstractClass says: I am doing the bulk of the work")

    def base_operation_2(self):
        print("AbstractClass says: But I let subclasses override some operations")

    def base_operation_3(self):
        print("AbstractClass says: But I am doing the bulk of the work anyway")

    # These operations have to be implemented in subclasses.
    @abstractmethod
    def required_operations_1(self):
        pass
    
    @abstractmethod
    def required_operations_2(self):
        pass
    
    # Subclasses may override the hooks or not.
    # The hooks already have default (empty) implementation.
    # Hooks provide additional extension points in the algorithm
    def hook_1(self):
        pass
    
    def hook_2(self):
        pass


class ConcreteClass_1(AbstractClass):
    
    def required_operations_1(self):
        print("ConcreteClass_1 says: Implemented Operation_1")

    def required_operations_2(self):
        print("ConcreteClass_1 says: Implemented Operation_2")


class ConcreteClass_2(AbstractClass):

    def required_operations_1(self):
        print("ConcreteClass_2 says: Implemented Operation_1")

    def required_operations_2(self):
        print("ConcreteClass_2 says: Implemented Operation_2")

    def hook_1(self):
        print("ConcreteClass_2 says: Overridden Hook_1")


# Call the template method to execute the algorithm
ConcreteClass_1().template_method()
print()
ConcreteClass_2().template_method()
