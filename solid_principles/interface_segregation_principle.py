# https://www.enjoyalgorithms.com/blog/interface-segregation-principle



# Violation Explanation:
# The LEDModule class inherits from SmartHomeModule and is forced to implement methods like isOpen() and openDoor() that are irrelevant to its functionality (lights don’t open doors!).

# This violates the Interface Segregation Principle, which says:

# "Clients should not be forced to depend on interfaces they do not use."

from abc import ABC, abstractmethod

class SmartHomeModule(ABC):
    
    @abstractmethod
    def turn_on_light(self, light_id: int):
        pass

    @abstractmethod
    def turn_off_light(self, light_id: int):
        pass

    @abstractmethod
    def is_on(self, light_id: int):
        pass

    @abstractmethod
    def open_door(self, door_id: int):
        pass

    @abstractmethod
    def is_open(self, door_id: int):
        pass

    @abstractmethod
    def close_door(self, door_id: int):
        pass
    
# Here, any class inheriting SmartHomeModule must implement all methods, even if not applicable.


class LEDModule(SmartHomeModule):
    
    def __init__(self):
        self.is_power_on = False
    
    def turn_on_light(self, light_id: int):
        self.is_power_on = True
    
    def turn_off_light(self, light_id: int):
        self.is_power_on = False
    
    def is_on(self, light_id: int):
        return self.is_power_on

    def open_door(self, door_id: int):
        raise NotImplementedError

    def is_open(self, door_id: int):
        raise NotImplementedError

    def close_door(self, door_id: int):
        raise NotImplementedError


# We forced to implement interfaces that are not required. such types of funcationally overloaded interface are Fat Interfaces

# We call an interface ‘fat’ if the interface can be broken down into groups of logically cohesive functions and each group serves a certain subset of clients.


#  Fat interfaces lead to:
# Unnecessary dependencies – Classes are forced to depend on methods they don’t use.

# Reduced cohesion – Interfaces try to do too much instead of focusing on a single responsibility.

# Fragile code – Changes in unrelated parts of the interface may impact all implementers.

# Difficult testing – Mocking unused methods or dealing with irrelevant functionality increases testing overhead.

# Poor readability and maintainability – It becomes harder to understand which parts of the interface are relevant to which clients.



################## Correct Version ########################


class SmartHomeInterface(ABC):
    
    @abstractmethod
    def is_active(self, device_id: int) -> bool:
        pass
    
    @abstractmethod
    def enable(self, device_id: int):
        pass

    @abstractmethod
    def disable(self, device_id: int):
        pass

class SmartDoorInterface(SmartHomeInterface):
    
    @abstractmethod
    def open_door(self, device_id: int):
        pass

    @abstractmethod
    def close_door(self, device_id: int):
        pass

class BasicDoor(SmartDoorInterface):
    def __init__(self): 
        self.status = {}

    def is_active(self, device_id: int) -> bool:
        return self.status.get(device_id, False)

    def enable(self, device_id: int):
        self.status[device_id] = True
    
    def disable(self, device_id: int):
        self.status[device_id] = False

    def open_door(self, device_id: int):
        self.enable(device_id)
        print(f"Door {device_id} opened")

    def close_door(self, device_id: int):
        self.disable(device_id)
        print(f"Door {device_id} closed")
    

###### Remote

class Remote(ABC):
    def __init__(self, smart_home_interface: SmartHomeInterface):
        self.smart_home_interface = smart_home_interface

    @abstractmethod
    def on_button_click(self, device_id: int):
        pass

class DoorRemote(Remote):
    
    def __init__(self, smart_door_interface: SmartDoorInterface):
        super().__init__(smart_door_interface)
        self.smart_door_interface  = smart_door_interface
    
    def on_button_click(self, device_id: int):
        if self.smart_door_interface.is_active(device_id):
            self.smart_door_interface.close_door(device_id)
        else:
            self.smart_door_interface.open_door(device_id)


# Demo

door = BasicDoor()

door_remote = DoorRemote(door)

door_remote.on_button_click(2)
door_remote.on_button_click(1)




# LED Interface extending base SmartHomeInterface
class SmartLEDInterface(SmartHomeInterface):

    @abstractmethod
    def turn_on(self, device_id: int):
        pass

    @abstractmethod
    def turn_off(self, device_id: int):
        pass


# Concrete implementation of SmartLEDInterface
class BasicLED(SmartLEDInterface):
    def __init__(self):
        self.status = {}

    def is_active(self, device_id: int) -> bool:
        return self.status.get(device_id, False)

    def enable(self, device_id: int):
        self.status[device_id] = True

    def disable(self, device_id: int):
        self.status[device_id] = False

    def turn_on(self, device_id: int):
        self.enable(device_id)
        print(f"LED {device_id} turned ON")

    def turn_off(self, device_id: int):
        self.disable(device_id)
        print(f"LED {device_id} turned OFF")


# Remote for LED lights
class LEDRemote(Remote):

    def __init__(self, smart_led_interface: SmartLEDInterface):
        super().__init__(smart_led_interface)
        self.smart_led_interface = smart_led_interface

    def on_button_click(self, device_id: int):
        if self.smart_led_interface.is_active(device_id):
            self.smart_led_interface.turn_off(device_id)
        else:
            self.smart_led_interface.turn_on(device_id)


# Demo
led = BasicLED()
led_remote = LEDRemote(led)

led_remote.on_button_click(1)  # should turn on
led_remote.on_button_click(1)  # should turn off
led_remote.on_button_click(2)  # should turn on
