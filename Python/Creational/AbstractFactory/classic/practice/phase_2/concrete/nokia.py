from abstract import AbstractProductFactory
from abstract import AbstractPhone


# Concrete Factory
class NokiaFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        raise Exception
    
    def make_radio(self, version):
        raise Exception
    
    def make_phone(self, model):
        return _NokiaPhone(model=model)
    
    def make_camera(self, mega_pixels):
        raise Exception
    
    def make_vacuum_cleaner(self, model_number):
        raise Exception
    
    def make_laundry(self, generation):
        raise Exception
    
    def make_fridge(self, type_):
        raise Exception


# Concrete Products
class _NokiaPhone(AbstractPhone):
    
    @property
    def weight(self):
        return '__MORE_THAN_OTHERS__'
    
    @property
    def average_life_span(self):
        return '__NEWER_DIE__'
    
    @property
    def warranty_expiration_date(self):
        return '__NO_NEED__'
    
    def turn_on(self):
        print('Another legend ...')
    
    def turn_off(self):
        print('Boss wanna rest')

    def call(self, number):
        print('__CONNECTING_PEOPLE__')
    
    def reject_call(self):
        print('Disconnecting people !!!')
