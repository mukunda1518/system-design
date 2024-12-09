from abc import ABC, abstractmethod

class LightingSystemInterface(ABC):
    @abstractmethod
    def turn_on_lights(self):
        pass

    @abstractmethod
    def turn_off_lights(self):
        pass

class ThermostatSystemInterface(ABC):
    @abstractmethod
    def set_temperature(self, temperature: int):
        pass

class SecuritySystemInterface(ABC):
    @abstractmethod
    def arm_security(self):
        pass

    @abstractmethod
    def disarm_security(self):
        pass


class LightingSystem(LightingSystemInterface):
    def turn_on_lights(self):
        print("Lights are ON.")

    def turn_off_lights(self):
        print("Lights are OFF.")

class ThermostatSystem(ThermostatSystemInterface):
    def set_temperature(self, temperature: int):
        print(f"Thermostat set to {temperature}°C.")

class SecuritySystem(SecuritySystemInterface):
    def arm_security(self):
        print("Security system is ARMED.")

    def disarm_security(self):
        print("Security system is DISARMED.")


class HomeAutomationFacadeInterface(ABC):
    @abstractmethod
    def leaving_home(self):
        pass

    @abstractmethod
    def arriving_home(self):
        pass


class HomeAutomationFacade(HomeAutomationFacadeInterface):
    def __init__(self, lighting: LightingSystemInterface, thermostat: ThermostatSystemInterface, security: SecuritySystemInterface):
        self.lighting = lighting
        self.thermostat = thermostat
        self.security = security

    def leaving_home(self):
        print("Executing 'Leaving Home' routine:")
        self.lighting.turn_off_lights()
        self.thermostat.set_temperature(18)  # Energy-saving temperature
        self.security.arm_security()

    def arriving_home(self):
        print("Executing 'Arriving Home' routine:")
        self.lighting.turn_on_lights()
        self.thermostat.set_temperature(22)  # Comfortable temperature
        self.security.disarm_security()



# The client interacts only with the facade interface and is unaware of the subsystem details or the concrete facade implementation.
# The facade provides a simple interface to the client that abstracts away the complexities of the subsystems.


if __name__ == "__main__":
    # Instantiate concrete subsystems
    lighting = LightingSystem()
    thermostat = ThermostatSystem()
    security = SecuritySystem()

    # Use the concrete facade class, which implements the interface
    facade: HomeAutomationFacadeInterface = HomeAutomationFacade(lighting, thermostat, security)

    # Perform operations via facade
    facade.leaving_home()
    print()
    facade.arriving_home()