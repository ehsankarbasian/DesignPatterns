from abstract import AbstractProductFactory
from abstract import AbstractTV, AbstractRadio, AbstractPhone, AbstractCamera, AbstractVacuumCleaner, AbstractLaundry, AbstractFridge


# Concrete Factory
class SamaungFactory(AbstractProductFactory):
    
    def make_tv(self, diameter):
        return _SamsungTv(diameter)
    
    def make_radio(self, version):
        return _SamsungRadio(version=version)
    
    def make_phone(self, model):
        return _SamsungPhone(model=model)
    
    def make_camera(self, mega_pixels):
        return _SamsungCamera(mega_pixels=mega_pixels)
    
    def make_vacuum_cleaner(self, model_number):
        return _SamsungVacuumCleaner(model_number=model_number)
    
    def make_laundry(self, generation):
        return _SamsungLaundry(generation=generation)
    
    def make_fridge(self, type_):
        return _SamsungFridge(type_=type_)


# Concrete Products
class _SamsungTv(AbstractTV):
    
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


class _SamsungRadio(AbstractRadio):
    
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


class _SamsungPhone(AbstractPhone):
    
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


class _SamsungCamera(AbstractCamera):
    
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


class _SamsungVacuumCleaner(AbstractVacuumCleaner):
    
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

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    def set_level(self):
        pass
    
    def restract_cord(self):
        pass


class _SamsungLaundry(AbstractLaundry):
    
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

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    @property
    def capacity(self):
        pass
    
    def set_program(self):
        pass


class _SamsungFridge(AbstractFridge):
    
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

    @property
    def power(self):
        pass
    
    @property
    def grade(self):
        pass
    
    @property
    def color(self):
        pass
    
    def make_clean(self):
        pass
    
    @property
    def feet_tall(self):
        pass
    
    @property
    def temperature(self):
        pass
    
    def boost(self):
        pass
