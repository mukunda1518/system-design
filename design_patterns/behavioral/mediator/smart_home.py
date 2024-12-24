from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import datetime

class SmartHomeMediator:
    def __init__(self):
        self._components: Dict[str, 'SmartDevice'] = {}
        self._scenes: Dict[str, List[str]] = {
            "movie_time": ["lights", "tv", "thermostat"],
            "good_morning": ["lights", "thermostat", "coffee_maker"],
            "sleep_mode": ["lights", "tv", "thermostat"]
        }
    
    def register_component(self, component: 'SmartDevice'):
        self._components[component.name] = component
        
    def activate_scene(self, scene: str):
        if scene not in self._scenes:
            raise ValueError(f"Scene {scene} not found")
            
        print(f"\nActivating {scene} scene at {datetime.now().strftime('%H:%M')}")
        
        if scene == "movie_time":
            self._components["lights"].dim(20)
            self._components["tv"].power_on()
            self._components["thermostat"].set_temperature(22)
            
        elif scene == "good_morning":
            self._components["lights"].set_brightness(100)
            self._components["thermostat"].set_temperature(24)
            self._components["coffee_maker"].start_brewing()
            
        elif scene == "sleep_mode":
            self._components["lights"].power_off()
            self._components["tv"].power_off()
            self._components["thermostat"].set_temperature(20)
    
    def component_changed(self, component: 'SmartDevice', state: dict):
        print(f"\nState change detected from {component.name}")
        
        # Handle interdependent behaviors
        if component.name == "motion_sensor" and state.get("motion_detected"):
            if datetime.now().hour < 6:  # Night time
                self._components["lights"].dim(10)
            else:
                self._components["lights"].set_brightness(100)
                
        elif component.name == "thermostat":
            temp = state.get("temperature")
            if temp > 25:
                self._components["ac"].power_on()
            elif temp < 20:
                self._components["ac"].power_off()

class SmartDevice(ABC):
    def __init__(self, mediator: SmartHomeMediator, name: str):
        self._mediator = mediator
        self.name = name
        self._state = {}
        mediator.register_component(self)
    
    def notify_mediator(self):
        self._mediator.component_changed(self, self._state)

class SmartLights(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "lights")
        self._state = {"power": False, "brightness": 0}
    
    def power_on(self):
        self._state["power"] = True
        print(f"Lights turned on")
        self.notify_mediator()
    
    def power_off(self):
        self._state["power"] = False
        print(f"Lights turned off")
        self.notify_mediator()
    
    def dim(self, level: int):
        self._state["brightness"] = level
        print(f"Lights dimmed to {level}%")
        self.notify_mediator()
    
    def set_brightness(self, level: int):
        self._state["brightness"] = level
        print(f"Lights brightness set to {level}%")
        self.notify_mediator()

class SmartThermostat(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "thermostat")
        self._state = {"temperature": 22, "mode": "auto"}
    
    def set_temperature(self, temp: float):
        self._state["temperature"] = temp
        print(f"Thermostat set to {temp}°C")
        self.notify_mediator()

class SmartTV(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "tv")
        self._state = {"power": False, "input": "hdmi1"}
    
    def power_on(self):
        self._state["power"] = True
        print("TV turned on")
        self.notify_mediator()
    
    def power_off(self):
        self._state["power"] = False
        print("TV turned off")
        self.notify_mediator()

class MotionSensor(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "motion_sensor")
        self._state = {"motion_detected": False}
    
    def detect_motion(self):
        self._state["motion_detected"] = True
        print("Motion detected!")
        self.notify_mediator()

class CoffeeMaker(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "coffee_maker")
        self._state = {"brewing": False}
    
    def start_brewing(self):
        self._state["brewing"] = True
        print("Starting coffee brew")
        self.notify_mediator()

class AC(SmartDevice):
    def __init__(self, mediator: SmartHomeMediator):
        super().__init__(mediator, "ac")
        self._state = {"power": False}
    
    def power_on(self):
        self._state["power"] = True
        print("AC turned on")
        self.notify_mediator()
    
    def power_off(self):
        self._state["power"] = False
        print("AC turned off")
        self.notify_mediator()

# Usage example
if __name__ == "__main__":
    # Create mediator and components
    mediator = SmartHomeMediator()
    lights = SmartLights(mediator)
    tv = SmartTV(mediator)
    thermostat = SmartThermostat(mediator)
    motion_sensor = MotionSensor(mediator)
    coffee_maker = CoffeeMaker(mediator)
    ac = AC(mediator)
    
    # Test scene activation
    mediator.activate_scene("movie_time")
    
    # Test motion detection at night
    motion_sensor.detect_motion()
    
    # Test temperature-based AC control
    thermostat.set_temperature(26)  # Should trigger AC