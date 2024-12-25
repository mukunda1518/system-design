from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    name: str
    price: float
    rating: float
    
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, rating={self.rating})"

# Strategy Interface
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, products: List[Product]) -> List[Product]:
        pass

# Concrete Strategies
class SortByName(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda x: x.name)

class SortByPrice(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda x: x.price)

class SortByRating(SortingStrategy):
    def sort(self, products: List[Product]) -> List[Product]:
        return sorted(products, key=lambda x: x.rating, reverse=True)  # Higher ratings first

# Context class that uses the strategy
class EcommercePlatform:
    def __init__(self, sorting_strategy: SortingStrategy = None):
        self.products = []
        self.sorting_strategy = sorting_strategy or SortByName()  # Default strategy
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def set_sorting_strategy(self, strategy: SortingStrategy):
        self.sorting_strategy = strategy
    
    def get_sorted_products(self) -> List[Product]:
        return self.sorting_strategy.sort(self.products)

# Example usage
def main():
    # Create platform instance
    platform = EcommercePlatform()
    
    # Add some products
    platform.add_product(Product("Laptop", 999.99, 4.5))
    platform.add_product(Product("Mouse", 29.99, 4.8))
    platform.add_product(Product("Keyboard", 59.99, 4.2))
    platform.add_product(Product("Monitor", 299.99, 4.7))
    
    # Sort by different strategies
    print("Sorting by name:")
    platform.set_sorting_strategy(SortByName())
    print(platform.get_sorted_products())
    
    print("\nSorting by price:")
    platform.set_sorting_strategy(SortByPrice())
    print(platform.get_sorted_products())
    
    print("\nSorting by rating:")
    platform.set_sorting_strategy(SortByRating())
    print(platform.get_sorted_products())

if __name__ == "__main__":
    main()