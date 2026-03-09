from abstract import AbstractPhoneFactory
from abstract import AbstractPhone


# Concrete Factory
class NokiaFactory(AbstractPhoneFactory):
    
    def make_phone(self, model):
        return _NokiaPhone(model=model)


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
