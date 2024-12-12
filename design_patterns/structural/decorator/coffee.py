from abc import ABC, abstractmethod


# Component Interface
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

# Concrete Component
class BasicCoffee(Coffee):
    def cost(self) -> float:
        return 2.0  # Base cost of coffee

    def description(self) -> str:
        return "Basic Coffee"


# Decorator Base Class
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()

# Concrete Decorator
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5  # Additional cost for milk

    def description(self) -> str:
        return self._coffee.description() + " with Milk"

# Concrete Decorator
class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.3  # Additional cost for sugar

    def description(self) -> str:
        return self._coffee.description() + " with Sugar"

# Concrete Decorator
class CaramelDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 1.0  # Additional cost for caramel

    def description(self) -> str:
        return self._coffee.description() + " with Caramel"


# Client Code
if __name__ == "__main__":
    
    basic_coffee = BasicCoffee()
    print(f"{basic_coffee.description()} costs ${basic_coffee.cost()}")

    coffe_with_milk = MilkDecorator(basic_coffee)
    print(f"{coffe_with_milk.description()} costs ${coffe_with_milk.cost()}")

    coffee_with_milk_and_sugar = SugarDecorator(coffe_with_milk)
    print(f"{coffee_with_milk_and_sugar.description()} costs ${coffee_with_milk_and_sugar.cost()}")

    fancy_coffee = CaramelDecorator(coffee_with_milk_and_sugar)
    print(f"{fancy_coffee.description()} costs ${fancy_coffee.cost()}")
    
