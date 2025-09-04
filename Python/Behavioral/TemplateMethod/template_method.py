from abc import ABC, abstractmethod


# Template abstract classs
class AbstractBuilder(ABC):
    
    # Template method
    def build(self):
        self.test()
        self.lint()
        self.assemble()
        self.deploy()
    
    @abstractmethod
    def test(self):
        pass
    
    @abstractmethod
    def lint(self):
        pass
    
    @abstractmethod
    def assemble(self):
        pass
    
    @abstractmethod
    def deploy(self):
        pass


# Template implementation 1
class AndroidBuilder(AbstractBuilder):
    
    def test(self):
        print('Running Andriod test')
    
    def lint(self):
        print('Linting the Android code')
    
    def assemble(self):
        print('Assembling the Android builder')
    
    def deploy(self):
        print('Deploying Android builer to server')


# Template implementation 2
class IosBuilder(AbstractBuilder):
    
    def test(self):
        print('Running ios tests')
    
    def lint(self):
        print('Linting the ios code')
    
    def assemble(self):
        print('Assembling the ios build')
    
    def deploy(self):
        print('Deploying ios build to server')


android_builder = AndroidBuilder()
android_builder.build()
print()
ios_builder = IosBuilder()
ios_builder.build()
