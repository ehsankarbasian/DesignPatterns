from abstract import AbstractProductFactory
from abstract import AbstractVacuumCleaner, AbstractLaundry, AbstractFridge


# Concrete Factory
class AzmayeshFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        raise Exception
    
    def make_radio(self, version):
        raise Exception
    
    def make_phone(self, model):
        raise Exception
    
    def make_camera(self, mega_pixels):
        raise Exception
    
    def make_vacuum_cleaner(self, model_number):
        pass
    
    def make_laundry(self, generation):
        pass
    
    def make_fridge(self, type_):
        pass
