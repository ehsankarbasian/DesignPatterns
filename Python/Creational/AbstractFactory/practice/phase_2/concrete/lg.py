from abstract import AbstractProductFactory
from abstract import AbstractTV, AbstractRadio, AbstractPhone, AbstractCamera


# Concrete Factory
class LgFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        return _LgTv(diameter=diameter)
    
    def make_radio(self, version):
        return _LgRadio(version=version)
    
    def make_phone(self, model):
        return _LgPhone(model=model)
    
    def make_camera(self, mega_pixels):
        return _LgCamera(mega_pixels=mega_pixels)
    
    def make_vacuum_cleaner(self, model_number):
        pass
    
    def make_laundry(self, generation):
        pass
    
    def make_fridge(self, type_):
        pass


# Concrete Products
class _LgTv(AbstractTV):
    
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


class _LgRadio(AbstractRadio):
    
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

    def set_mode(self, mode):
        self._mode = mode


class _LgPhone(AbstractPhone):
    
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


class _LgCamera(AbstractCamera):
    
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

    def take_picture(self):
        pass
    
    def take_film(self):
        pass
    
    def zoom_in(self):
        pass
    
    def zoom_out(self):
        pass
