# https://medium.com/@zackbunch/python-dependency-inversion-8096c2d5e46c


# Abstraction or Dependency Inversion if you’re familiar with SOLID principles.
# The basic idea of abstraction is as simple as looking at something like switches in your home.
# Your home may contain numerous switches that control lights, fans and even plumbing. As a user, you only care about an object being turned on or off when the switch is used. 
# You don’t care about what is happening behind the scenes.In code, we can model a lightbulb using a class as such


class LightBulb:
    def turn_on(self):
        print("Light bulb: turned on")
    def turn_off(self):
        print("Lightbulb: turned off")


class PowerSwitch:
    def __init__(self, l: LightBulb):
        self.light = l
        self.on = False
    
    def press(self):
        if self.on:
            self.light.turn_off()
            self.on = False
        else:
            self.light.turn_on()
            self.on = True



huebulb = LightBulb()
switch = PowerSwitch(huebulb)
switch.press()
switch.press()


# There is a clear dependency between the lightbulb and the power switch because the power switch object takes in a lightbulb and then directly calls the turn off and turn on method on that instance

# we need to ensure that high-level modules do not depend on low level modules, but instead depend on abstractions. The abstraction should not depend on details, instead the details should depend on abstractions

# To solve this we create an interface


from abc import ABC, abstractmethod

class Switchable(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class LightBulb(Switchable):
    def turn_on(self):
        print("Light bulb: turned on")
    def turn_off(self):
        print("Lightbulb: turned off")
        
class Fan(Switchable):
    def turn_on(self):
        print("Fan: turned on")
    def turn_off(self):
        print("Fan: turned off")

class PowerSwitch:
    def __init__(self, l: Switchable):
        self.light = l
        self.on = False
    
    def press(self):
        if self.on:
            self.light.turn_off()
            self.on = False
        else:
            self.light.turn_on()
            self.on = True

huebulb = LightBulb()
switch = PowerSwitch(huebulb)
switch.press()
switch.press()



# Removed the dependency between lightbulb and PowerSwitch. The PowerSwitch is now dependent on the Switchable class

#  By implementing dependency inversion, we now have decoupled two classes through an interface,
# which in our case is Switchable. It is now clear to see the usefulness that dependency inversion provides by reducing coupling between classes.