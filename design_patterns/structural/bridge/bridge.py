from abc import ABC, abstractmethod

# The "implementation" interface
class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool:
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def get_volume(self) -> int:
        pass

    @abstractmethod
    def set_volume(self, percent: int):
        pass

    @abstractmethod
    def get_channel(self) -> int:
        pass

    @abstractmethod
    def set_channel(self, channel: int):
        pass


# Concrete Implementation: TV
class Tv(Device):
    def __init__(self):
        self._enabled = False
        self._volume = 50
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._enabled

    def enable(self):
        self._enabled = True
        print("TV is now ON")

    def disable(self):
        self._enabled = False
        print("TV is now OFF")

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int):
        self._volume = max(0, min(100, percent))  # Clamp between 0 and 100
        print(f"TV volume set to {self._volume}")

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int):
        self._channel = channel
        print(f"TV channel set to {self._channel}")


# Concrete Implementation: Radio
class Radio(Device):
    def __init__(self):
        self._enabled = False
        self._volume = 30
        self._channel = 1

    def is_enabled(self) -> bool:
        return self._enabled

    def enable(self):
        self._enabled = True
        print("Radio is now ON")

    def disable(self):
        self._enabled = False
        print("Radio is now OFF")

    def get_volume(self) -> int:
        return self._volume

    def set_volume(self, percent: int):
        self._volume = max(0, min(100, percent))  # Clamp between 0 and 100
        print(f"Radio volume set to {self._volume}")

    def get_channel(self) -> int:
        return self._channel

    def set_channel(self, channel: int):
        self._channel = channel
        print(f"Radio channel set to {self._channel}")


# The "abstraction"
class RemoteControl:
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        if self.device.is_enabled():
            self.device.disable()
        else:
            self.device.enable()

    def volume_down(self):
        self.device.set_volume(self.device.get_volume() - 10)

    def volume_up(self):
        self.device.set_volume(self.device.get_volume() + 10)

    def channel_down(self):
        self.device.set_channel(self.device.get_channel() - 1)

    def channel_up(self):
        self.device.set_channel(self.device.get_channel() + 1)


# Refined Abstraction: AdvancedRemoteControl
class AdvancedRemoteControl(RemoteControl):
    def mute(self):
        self.device.set_volume(0)
        print("Device muted")


# Client Code
if __name__ == "__main__":
    # Using a TV with a simple remote
    tv = Tv()
    remote = RemoteControl(tv)
    print("Testing TV with Remote Control:")
    remote.toggle_power()
    remote.volume_up()
    remote.channel_up()
    remote.toggle_power()

    print("\nTesting Radio with Advanced Remote Control:")
    # Using a Radio with an advanced remote
    radio = Radio()
    advanced_remote = AdvancedRemoteControl(radio)
    advanced_remote.toggle_power()
    advanced_remote.volume_down()
    advanced_remote.mute()
    advanced_remote.toggle_power()