from abc import ABC, abstractmethod


# Abstract Class

class Beverage(ABC):
    
    def __init__(self):
        self.description = "Unknown Beverage"
    
    def get_description(self):
        return self.description

    @abstractmethod
    def cost(self):
        pass


# Concrete Beverages

class Expresso(Beverage):
    
    def __init__(self):
        self.description = "Expresso"

    def cost(self):
        return 1.99

class HouseBlend(Beverage):
    def __init__(self):
        self.description = "House Blend"

    def cost(self):
        return 0.89

class DrarkRoast(Beverage):
    def __init__(self):
        self.description = "Dark Roast"

    def cost(self):
        return 0.99


# Decorators

# Decorator Interface

class CondimentDecorator(Beverage):
    
    def __init__(self, beverage):
        self._beverage = beverage

    def get_description(self):
        pass

    def cost(self):
        pass

# Concrete Decorators

class Mocha(CondimentDecorator):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost() + 0.20

    def get_description(self):
        return self._beverage.get_description() + ", Mocha"

class Soy(CondimentDecorator):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost() + 0.15

    def get_description(self):
        return self._beverage.get_description() + ", Soy"


class Whip(CondimentDecorator):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    def cost(self):
        return self._beverage.cost() + 0.10

    def get_description(self):
        return self._beverage.get_description() + ", Whip"


if __name__ == "__main__":
    
    expresso_bevg = Expresso()
    
    print(expresso_bevg.get_description() + f" - $ {expresso_bevg.cost()}")
    
    darkroast = DrarkRoast()
    darkroast_w_mocha = Mocha(darkroast)
    darkroast_w_mocha_w_soy = Soy(darkroast_w_mocha)
    darkroast_w_mocha_w_soy_w_whip = Whip(darkroast_w_mocha_w_soy)
    print(darkroast_w_mocha_w_soy_w_whip.get_description() + f" - $ {darkroast_w_mocha_w_soy_w_whip.cost()}")
    