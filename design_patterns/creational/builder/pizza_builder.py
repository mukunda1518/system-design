from abc import ABC, abstractmethod


class Pizza:
    def __init__(self):
        self.dough = None
        self.base = None
        self.toppings = []
        self.sauce = None
        self.bake = None

    def set_dough(self, dough):
        self.dough = dough

    def set_base(self, base):
        self.base = base

    def set_toppings(self, toppings):
        self.toppings = toppings

    def set_sauce(self, sauce):
        self.sauce = sauce

    def set_bake (self, bake):
        self.bake = bake

    def __str__(self):
        return (f"Pizza with dough: {self.dough}, base: {self.base}, toppings: {self.toppings}, sauce: {self.sauce}, bake: {self.bake}")
    

# Abstract Builder

class PizzaBuilder(ABC):
    def __init__(self):
        self.pizza = Pizza()

    @abstractmethod
    def build_dough(self):
        pass

    @abstractmethod
    def build_base(self):
        pass

    @abstractmethod
    def build_toppings(self):
        pass

    @abstractmethod
    def build_sauce(self):
        pass

    @abstractmethod
    def build_bake(self):
        pass

    @abstractmethod
    def get_pizza(self):
        return self.pizza


# Concrete Builder 1: Veg Pizza

class VegPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.set_dough("Whole Wheat Dough")

    def build_base(self):
        self.pizza.set_base("Thin Crust")

    def build_toppings(self):
        self.pizza.set_toppings(["Onion", "Capsicum", "Tomato", "Cheese"])

    def build_sauce(self):
        self.pizza.set_sauce("Tomato Basil Sauce")

    def build_bake(self):
        self.pizza.set_bake("Baked at 200°C for 15 minutes")

    def get_pizza(self):
        return self.pizza


# Concrete Builder 2: Non-Veg Pizza

class NonVegPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.set_dough("Refined Flour Dough")

    def build_base(self):
        self.pizza.set_base("Hand Tossed")

    def build_toppings(self):
        self.pizza.set_toppings(["Cheese", "Chicken", "Bacon", "Pepperoni"])

    def build_sauce(self):
        self.pizza.set_sauce("BBQ Sauce")

    def build_bake(self):
        self.pizza.set_bake("Baked at 220°C for 20 minutes")

    def get_pizza(self):
        return self.pizza

# Concrete Builder 3: Supreme Pizza

class SupremePizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.set_dough("Pan Pizza Dough")

    def build_base(self):
        self.pizza.set_base("Spicy Tomato Sauce")

    def build_toppings(self):
        self.pizza.set_toppings(["Cheese", "Pepperoni", "Sausage", "Mushrooms", "Bell Peppers", "Onions"])

    def build_sauce(self):
        self.pizza.set_sauce("Spicy Tomato Sauce")

    def build_bake(self):
        self.pizza.set_bake("Baked at 220°C for 20 minutes")

    def get_pizza(self):
        return self.pizza


# Concrete Builder 4: Margherita Pizza

class MargheritaPizzaBuilder(PizzaBuilder):
    def build_dough(self):
        self.pizza.set_dough("Thin Crust Dough")

    def build_base(self):
        self.pizza.set_base("Tomato and Basil Sauce")

    def build_toppings(self):
        self.pizza.set_toppings(["Mozzarella", "Basil"])

    def build_sauce(self):
        self.pizza.set_sauce("Tomato and Basil Sauce")

    def build_bake(self):
        self.pizza.set_bake("Baked at 200°C for 15 minutes")

    def get_pizza(self):
        return self.pizza

# Director

class PizzaDirector:
    def __init__(self, builder: PizzaBuilder):
        self.builder = builder

    def make_pizza(self):
        self.builder.build_dough()
        self.builder.build_base()
        self.builder.build_toppings()
        self.builder.build_sauce()
        self.builder.build_bake()

    def get_pizza(self):
        return self.builder.get_pizza()


# Client Code

if __name__ == "__main__":
    # Veg Pizza
    veg_pizza_builder = VegPizzaBuilder()
    veg_pizza_director = PizzaDirector(veg_pizza_builder)
    veg_pizza_director.make_pizza()
    veg_pizza = veg_pizza_director.get_pizza()
    print(veg_pizza)

    # Non-Veg Pizza
    non_veg_pizza_builder = NonVegPizzaBuilder()
    non_veg_pizza_director = PizzaDirector(non_veg_pizza_builder)
    non_veg_pizza_director.make_pizza()
    non_veg_pizza = non_veg_pizza_director.get_pizza()
    print(non_veg_pizza)

    # Supreme Pizza
    supreme_pizza_builder = SupremePizzaBuilder()
    supreme_pizza_director = PizzaDirector(supreme_pizza_builder)
    supreme_pizza_director.make_pizza()
    supreme_pizza = supreme_pizza_director.get_pizza()
    print(supreme_pizza)

    # Margherita Pizza
    margherita_pizza_builder = MargheritaPizzaBuilder()
    margherita_pizza_director = PizzaDirector(margherita_pizza_builder)
    margherita_pizza_director.make_pizza()
    margherita_pizza = margherita_pizza_director.get_pizza()
    print(margherita_pizza)
    

