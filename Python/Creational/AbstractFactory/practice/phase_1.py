from abc import ABC, abstractmethod

'''
Implement products [
    TV,
    Radio,
    Phone,
    Camera
]
for the brands [
    Samsung,
    Sony
    LG,
]
'''


# Abstract Factory
class ProductFactory(ABC):
    
    @abstractmethod
    def make_tv(self):
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


# Concrete Factory (SAMSUNG)
class SamaungFactory(ProductFactory):
    
    def make_tv(self):
        pass
    
    def make_radio(self):
        pass
    
    def make_phone(self):
        pass
    
    def make_camera(self):
        pass


# Concrete Factory (SONY)
class SonyFactory(ProductFactory):
    
    def make_tv(self):
        pass
    
    def make_radio(self):
        pass
    
    def make_phone(self):
        pass
    
    def make_camera(self):
        pass


# Concrete Factory (LG)
class LgFactory(ProductFactory):
    
    def make_tv(self):
        pass
    
    def make_radio(self):
        pass
    
    def make_phone(self):
        pass
    
    def make_camera(self):
        pass


# Not a part of the pattern, just to DRY
class AbstractBaseProduct(ABC):
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
class AbstractMediaPlayerProduct(ABC):
    
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
class AbstractTV(AbstractBaseProduct, AbstractMediaPlayerProduct):
    
    @abstractmethod
    def increase_screen_brightness(self):
        pass
    
    @abstractmethod
    def decrease_screen_brightness(self):
        pass


class AbstractRadio(AbstractBaseProduct, AbstractMediaPlayerProduct):
    
    @abstractmethod
    def set_mode(self, mode):
        pass


class AbstractPhone(AbstractBaseProduct):
    
    @abstractmethod
    def call(self, number):
        pass
    
    @abstractmethod
    def reject_call(self):
        pass


class AbstractCamera(AbstractBaseProduct):
    
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


# Concrete Products (TV)
class SamsungTv(AbstractTV):
    
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


class SonyTv(AbstractTV):
    
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


class LgTv(AbstractTV):
    
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


# Concrete Products (Radio)
class SamsungRadio(AbstractRadio):
    
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
        pass


class SonyRadio(AbstractRadio):
    
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
        pass


class LgRadio(AbstractRadio):
    
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
        pass


# Concrete Products (Phone)
class SamsungPhone(AbstractPhone):
    
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


class SonyPhone(AbstractPhone):
    
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


class LgPhone(AbstractPhone):
    
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


# Concrete Products (Camera)
class SamsungCamera(AbstractCamera):
    
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


class SonyCamera(AbstractCamera):
    
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


class LgCamera(AbstractCamera):
    
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
