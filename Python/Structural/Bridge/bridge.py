from abc import ABC, abstractmethod


class Device(ABC):
    
    @property
    @abstractmethod
    def is_enabled(self):
        pass
    
    @abstractmethod
    def enable(self):
        pass
    
    @abstractmethod
    def disable(self):
        pass
    
    @abstractmethod
    def get_volume(self):
        pass
    
    @abstractmethod
    def set_volume(self, percent):
        pass
    
    @abstractmethod
    def get_channel(self):
        pass
    
    @abstractmethod
    def set_channel(self):
        pass


class TV(Device):
    
    def __init__(self):
        self._is_enabled = False
        self._volume = 0
        self._channel = 1
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    def enable(self):
        self._is_enabled = True
    
    def disable(self):
        self._is_enabled = False
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        valid_percent = 0 if percent < 0 else percent
        self._volume = valid_percent
    
    def get_channel(self):
        return self._channel
    
    def set_channel(self, channel):
        valid_channel = 1 if channel < 1 else channel
        self._channel = valid_channel


class Radio(Device):
    
    def __init__(self):
        self._is_enabled = False
        self._volume = 0
        self._channel = 1
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    def enable(self):
        self._is_enabled = True
    
    def disable(self):
        self._is_enabled = False
    
    def get_volume(self):
        return self._volume
    
    def set_volume(self, percent):
        valid_percent = 0 if percent < 0 else percent
        self._volume = valid_percent
    
    def get_channel(self):
        return self._channel
    
    def set_channel(self, channel):
        valid_channel = 1 if channel < 1 else channel
        self._channel = valid_channel


class RemoteControl:
    
    def __init__(self, device):
        self.__device = device
    
    def toggle_power(self):
        if self.__device.is_enabled:
            self.__device.disable()
        else:
            self.__device.enable()
    
    def volume_down(self):
        self.__device.set_volume(self.__device.get_volume() - 10)
    
    def volume_up(self):
        self.__device.set_volume(self.__device.get_volume() + 10)
    
    def channel_down(self):
        self.__device.set_channel(self.__device.get_channel() - 1)
    
    def channel_up(self):
        self.__device.set_channel(self.__device.get_channel() + 1)


class ExtendedRemoteControl(RemoteControl):
    
    def mute(self):
        self.__device.set_volume(0)


tv = TV()
remote = RemoteControl(tv)
remote.toggle_power()

radio = Radio()
remote = ExtendedRemoteControl(radio)
