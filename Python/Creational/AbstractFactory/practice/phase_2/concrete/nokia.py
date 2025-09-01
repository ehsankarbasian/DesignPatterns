from abstract import AbstractProductFactory
from abstract import AbstractTV, AbstractPhone


# Concrete Factory
class NokiaFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        pass
    
    def make_radio(self, version):
        raise Exception
    
    def make_phone(self, model):
        pass
    
    def make_camera(self, mega_pixels):
        raise Exception
    
    def make_vacuum_cleaner(self, model_number):
        raise Exception
    
    def make_laundry(self, generation):
        raise Exception
    
    def make_fridge(self, type_):
        raise Exception
