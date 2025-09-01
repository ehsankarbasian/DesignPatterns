from abc import ABC, abstractmethod


# Abstract Factory
class ProductFactory(ABC):
    
    @abstractmethod
    def make_tv(self, diameter):
        pass
    
    @abstractmethod
    def make_radio(self):
        pass
    
    @abstractmethod
    def make_phone(self):
        pass
    
    @abstractmethod
    def make_camera(self):
        pass


# Not a part of the pattern, just to DRY
class _AbstractBaseProduct(ABC):
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


# Abstract Products (TV, Radio, Phone, Camera)
class AbstractTV(_AbstractBaseProduct, _AbstractMediaPlayerProduct):
    
    def __init__(self, diameter):
        self._diameter = diameter
        super().__init__()
    
    @abstractmethod
    def increase_screen_brightness(self):
        pass
    
    @abstractmethod
    def decrease_screen_brightness(self):
        pass


class AbstractRadio(_AbstractBaseProduct, _AbstractMediaPlayerProduct):
    
    @abstractmethod
    def set_mode(self, mode):
        pass


class AbstractPhone(_AbstractBaseProduct):
    
    @abstractmethod
    def call(self, number):
        pass
    
    @abstractmethod
    def reject_call(self):
        pass


class AbstractCamera(_AbstractBaseProduct):
    
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
