from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    
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


class DeviceOperationPrinter:
    """
    It's a helper, not a part of the pattern
    """
    
    @property
    def _class_name(self):
        return self.__class__.__name__
    
    def _print_operation(self, what_happend):
        print(f'"{self._class_name}" {what_happend}')


class TV(AbstractDevice, DeviceOperationPrinter):
    
    def __init__(self):
        self._is_enabled = False
        self._volume = 0
        self._channel = 1
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    def enable(self):
        self._is_enabled = True
        self._print_operation('is enabled')
    
    def disable(self):
        self._is_enabled = False
        self._print_operation('is disabled')
    
    def get_volume(self):
        self._print_operation('volume is getted')
        return self._volume
    
    def set_volume(self, percent):
        valid_percent = 0 if percent < 0 else percent
        self._volume = valid_percent
        self._print_operation(f'volume is setted: {valid_percent}')
    
    def get_channel(self):
        self._print_operation('channel is getted')
        return self._channel
    
    def set_channel(self, channel):
        valid_channel = 1 if channel < 1 else channel
        self._channel = valid_channel
        self._print_operation(f'channel is setted: {valid_channel}')


class Radio(AbstractDevice, DeviceOperationPrinter):
    
    def __init__(self):
        self._is_enabled = False
        self._volume = 0
        self._channel = 1
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    def enable(self):
        self._is_enabled = True
        self._print_operation('is enabled')
    
    def disable(self):
        self._is_enabled = False
        self._print_operation('is disabled')
    
    def get_volume(self):
        self._print_operation('volume is getted')
        return self._volume
    
    def set_volume(self, percent):
        valid_percent = 0 if percent < 0 else percent
        self._volume = valid_percent
        self._print_operation(f'volume is setted: {valid_percent}')
    
    def get_channel(self):
        self._print_operation('channel is getted')
        return self._channel
    
    def set_channel(self, channel):
        valid_channel = 1 if channel < 1 else channel
        self._channel = valid_channel
        self._print_operation(f'channel is setted: {valid_channel}')


class RemoteOperationPrinter:
    """
    It's a helper, not a part of the pattern
    """
    
    @property
    def _class_name(self):
        return self.__class__.__name__
    
    @property
    def _device_name(self):
        return self._device.__class__.__name__
    
    def _print_operation(self, what):
        print(f'"{self._class_name}" {what} the "{self._device_name}"')


class RemoteControl(RemoteOperationPrinter):
    
    def __init__(self, device):
        self._device = device
    
    def toggle_power(self):
        if self._device.is_enabled:
            self._device.disable()
        else:
            self._device.enable()
        self._print_operation('toggled power of')
    
    def volume_down(self):
        self._device.set_volume(self._device.get_volume() - 10)
        self._print_operation('volumed down')
    
    def volume_up(self):
        self._device.set_volume(self._device.get_volume() + 10)
        self._print_operation('volumed up')
    
    def channel_down(self):
        self._device.set_channel(self._device.get_channel() - 1)
        self._print_operation('switched down the channel of')
    
    def channel_up(self):
        self._device.set_channel(self._device.get_channel() + 1)
        self._print_operation('switched up the channel of')


class ExtendedRemoteControl(RemoteControl):
    
    def mute(self):
        self._device.set_volume(0)
        self._print_operation('setted volume 0 for')


tv = TV()
remote = RemoteControl(tv)
remote.toggle_power()
remote.volume_up()
remote.volume_up()
remote.volume_up()
remote.volume_down()
remote.channel_up()
remote.channel_up()
remote.channel_down()
remote.channel_down()
remote.channel_down()

print()
radio = Radio()
remote = ExtendedRemoteControl(radio)
remote.mute()
remote.volume_up()
remote.volume_up()
remote.volume_up()
remote.volume_down()
remote.channel_up()
remote.channel_up()
remote.channel_down()
remote.channel_down()
remote.channel_down()
