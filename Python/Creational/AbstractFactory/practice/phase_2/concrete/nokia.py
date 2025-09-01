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


class _NokiaTv(AbstractTV):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        pass
    
    @property
    def warranty_expiration_date(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

    def channel_up(self):
        pass
    
    def channel_down(self):
        pass
    
    def volume_up(self):
        pass
    
    def volume_down(self):
        pass
    
    def mute(self):
        pass
    
    def unmute(self):
        pass

    def increase_screen_brightness(self):
        pass
    
    def decrease_screen_brightness(self):
        pass


class _NokiaPhone(AbstractPhone):
    
    @property
    def weight(self):
        pass
    
    @property
    def average_life_span(self):
        pass
    
    @property
    def warranty_expiration_date(self):
        pass
    
    def turn_on(self):
        pass
    
    def turn_off(self):
        pass

    def call(self, number):
        pass
    
    def reject_call(self):
        pass
