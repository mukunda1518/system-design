from abc import ABC, abstractmethod
from typing import List
import time

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

# Receiver classes
class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
        self.brightness = 0
    
    def turn_on(self) -> None:
        self.is_on = True
        print(f"{self.location} light turned on")
    
    def turn_off(self) -> None:
        self.is_on = False
        print(f"{self.location} light turned off")
    
    def dim(self, level: int) -> None:
        self.brightness = level
        print(f"{self.location} light dimmed to {level}%")

class Thermostat:
    def __init__(self, location: str):
        self.location = location
        self.temperature = 20
    
    def set_temperature(self, temperature: int) -> None:
        self.temperature = temperature
        print(f"{self.location} thermostat set to {temperature}°C")

# Concrete Commands
class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.turn_on()
    
    def undo(self) -> None:
        self.light.turn_off()

class LightDimCommand(Command):
    def __init__(self, light: Light, level: int):
        self.light = light
        self.level = level
        self.prev_level = light.brightness
    
    def execute(self) -> None:
        self.prev_level = self.light.brightness
        self.light.dim(self.level)
    
    def undo(self) -> None:
        self.light.dim(self.prev_level)

class ThermostatCommand(Command):
    def __init__(self, thermostat: Thermostat, temperature: int):
        self.thermostat = thermostat
        self.temperature = temperature
        self.prev_temperature = thermostat.temperature
    
    def execute(self) -> None:
        self.prev_temperature = self.thermostat.temperature
        self.thermostat.set_temperature(self.temperature)
    
    def undo(self) -> None:
        self.thermostat.set_temperature(self.prev_temperature)

# Command Invoker
class SmartHomeController:
    def __init__(self):
        self._commands: List[Command] = []
        self._command_history: List[Command] = []
    
    def add_command(self, command: Command) -> None:
        self._commands.append(command)
    
    def execute_commands(self) -> None:
        for command in self._commands:
            command.execute()
            self._command_history.append(command)
        self._commands.clear()
    
    def undo_last(self) -> None:
        if self._command_history:
            command = self._command_history.pop()
            command.undo()

# Example usage
def main():
    # Create receivers
    living_room_light = Light("Living Room")
    bedroom_light = Light("Bedroom")
    living_room_thermostat = Thermostat("Living Room")
    
    # Create commands
    light_on = LightOnCommand(living_room_light)
    bedroom_dim = LightDimCommand(bedroom_light, 50)
    set_temp = ThermostatCommand(living_room_thermostat, 22)
    
    # Create controller and add commands
    controller = SmartHomeController()
    controller.add_command(light_on)
    controller.add_command(bedroom_dim)
    controller.add_command(set_temp)
    
    # Execute all commands
    print("Executing evening mode commands...")
    controller.execute_commands()
    
    time.sleep(2)  # Simulate some time passing
    
    # Undo last command
    print("\nUndo last command...")
    controller.undo_last()  # Will undo thermostat setting
    controller.undo_last()  # Will undo bedroom dimming

if __name__ == "__main__":
    main()