from abstract import ProductFactory
from abstract import AbstractTV, AbstractRadio, AbstractPhone, AbstractCamera


# Concrete Factory
class SonyFactory(ProductFactory):
    
    def make_tv(self, diameter):
        return _SonyTv(diameter=diameter)
    
    def make_radio(self, version):
        return _SonyRadio(version=version)
    
    def make_phone(self, model):
        return _SonyPhone(model=model)
    
    def make_camera(self, mega_pixels):
        return _SonyCamera(mega_pixels=mega_pixels)


# Concrete products
class _SonyTv(AbstractTV):
    
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


class _SonyRadio(AbstractRadio):
    
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


class _SonyPhone(AbstractPhone):
    
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


class _SonyCamera(AbstractCamera):
    
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
