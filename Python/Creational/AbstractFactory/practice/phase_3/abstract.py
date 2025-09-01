from abc import ABC, abstractmethod
from logger import LogMethodCallsMixin


# Abstract Factory
class AbstractProductFactory(ABC):
    
    @abstractmethod
    def make_tv(self, diameter):
        pass
    
    @abstractmethod
    def make_radio(self, version):
        pass
    
    @abstractmethod
    def make_phone(self, model):
        pass
    
    @abstractmethod
    def make_camera(self, mega_pixels):
        pass
    
    @abstractmethod
    def make_vacuum_cleaner(self, model_number):
        pass
    
    @abstractmethod
    def make_laundry(self, generation):
        pass
    
    @abstractmethod
    def make_fridge(self, type_):
        pass


# Not a part of the pattern, just to DRY
class _AbstractBaseProduct(ABC, LogMethodCallsMixin):
    
    @property
    @abstractmethod
    def weight(self):
        pass
    
    @property
    @abstractmethod
    def average_life_span(self):
        pass
    
    @property
    @abstractmethod
    def warranty_expiration_date(self):
        pass
    
    @abstractmethod
    def turn_on(self):
        pass
    
    @abstractmethod
    def turn_off(self):
        pass


# Not a part of the pattern, just to DRY
class _AbstractMediaPlayerProduct(ABC):
    
    @abstractmethod
    def channel_up(self):
        pass
    
    @abstractmethod
    def channel_down(self):
        pass
    
    @abstractmethod
    def volume_up(self):
        pass
    
    @abstractmethod
    def volume_down(self):
        pass
    
    @abstractmethod
    def mute(self):
        pass
    
    @abstractmethod
    def unmute(self):
        pass


# Not a part of the pattern, just to DRY
class _AbstractHomeApplianceProduct(ABC):
    
    @property
    @abstractmethod
    def power(self):
        pass
    
    @property
    @abstractmethod
    def grade(self):
        pass
    
    @property
    @abstractmethod
    def color(self):
        pass
    
    @abstractmethod
    def make_clean(self):
        pass


# Abstract Products (TV, Radio, Phone, Camera)
class AbstractTV(_AbstractBaseProduct, _AbstractMediaPlayerProduct):
    
    def __init__(self, diameter):
        self._diameter = diameter
        super().__init__()
    
    @property
    def diameter(self):
        return self._diameter
    
    @abstractmethod
    def increase_screen_brightness(self):
        pass
    
    @abstractmethod
    def decrease_screen_brightness(self):
        pass


class AbstractRadio(_AbstractBaseProduct, _AbstractMediaPlayerProduct):
    
    def __init__(self, version):
        self._version = version
        super().__init__()
    
    @property
    def version(self):
        return self._version
    
    @abstractmethod
    def set_mode(self, mode):
        pass


class AbstractPhone(_AbstractBaseProduct):
    
    def __init__(self, model):
        self._model = model
        super().__init__()
    
    @property
    def model(self):
        return self._model
    
    @abstractmethod
    def call(self, number):
        pass
    
    @abstractmethod
    def reject_call(self):
        pass


class AbstractCamera(_AbstractBaseProduct):
    
    def __init__(self, mega_pixels):
        self._mega_pixels = mega_pixels
        super().__init__()
    
    @property
    def mega_pixels(self):
        return self._mega_pixels
    
    @abstractmethod
    def take_picture(self):
        pass
    
    @abstractmethod
    def take_film(self):
        pass
    
    @abstractmethod
    def zoom_in(self):
        pass
    
    @abstractmethod
    def zoom_out(self):
        pass


class AbstractVacuumCleaner(_AbstractBaseProduct, _AbstractHomeApplianceProduct):
    
    def __init__(self, model_number):
        self._model_number = model_number
        super().__init__()
    
    @property
    def model_number(self):
        return self._model_number
    
    @abstractmethod
    def set_level(self):
        pass
    
    @abstractmethod
    def restract_cord(self):
        pass


class AbstractLaundry(_AbstractBaseProduct, _AbstractHomeApplianceProduct):
    
    def __init__(self, generation):
        self._generation = generation
        super().__init__()
    
    @property
    def generation(self):
        return self._generation
    
    @property
    @abstractmethod
    def capacity(self):
        pass
    
    @abstractmethod
    def set_program(self):
        pass


class AbstractFridge(_AbstractBaseProduct, _AbstractHomeApplianceProduct):
    
    def __init__(self, type_):
        self._type_ = type_
        super().__init__()
    
    @property
    def type_(self):
        return self._type_
    
    @property
    @abstractmethod
    def feet_tall(self):
        pass
    
    @property
    @abstractmethod
    def temperature(self):
        pass
    
    @abstractmethod
    def boost(self):
        pass
