from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Protocol, Optional
from enum import Enum

@dataclass
class Product:
    name: str
    price: float
    rating: float
    category: str
    date_added: str  # ISO format date string
    stock: int
    
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, rating={self.rating}, category='{self.category}')"

# Sorting Strategy Interface
class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, products: List[Product]) -> List[Product]:
        pass

# Enhanced Concrete Sorting Strategies
class SortDirection(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"

class ComplexSortStrategy(SortingStrategy):
    def __init__(self, primary_key: str, secondary_key: Optional[str] = None, 
                 direction: SortDirection = SortDirection.ASCENDING):
        self.primary_key = primary_key
        self.secondary_key = secondary_key
        self.direction = direction
    
    def sort(self, products: List[Product]) -> List[Product]:
        def sort_key(product):
            primary_value = getattr(product, self.primary_key)
            if self.secondary_key:
                secondary_value = getattr(product, self.secondary_key)
                return (primary_value, secondary_value)
            return primary_value
        
        reverse = self.direction == SortDirection.DESCENDING
        return sorted(products, key=sort_key, reverse=reverse)

# Filtering Strategy Interface
class FilterStrategy(ABC):
    @abstractmethod
    def filter(self, products: List[Product]) -> List[Product]:
        pass

# Concrete Filtering Strategies
class PriceRangeFilter(FilterStrategy):
    def __init__(self, min_price: float = 0, max_price: float = float('inf')):
        self.min_price = min_price
        self.max_price = max_price
    
    def filter(self, products: List[Product]) -> List[Product]:
        return [p for p in products if self.min_price <= p.price <= self.max_price]

class CategoryFilter(FilterStrategy):
    def __init__(self, categories: List[str]):
        self.categories = set(categories)
    
    def filter(self, products: List[Product]) -> List[Product]:
        return [p for p in products if p.category in self.categories]

class InStockFilter(FilterStrategy):
    def filter(self, products: List[Product]) -> List[Product]:
        return [p for p in products if p.stock > 0]

# Composite Filter Strategy
class CompositeFilter(FilterStrategy):
    def __init__(self, filters: List[FilterStrategy]):
        self.filters = filters
    
    def filter(self, products: List[Product]) -> List[Product]:
        result = products
        for filter_strategy in self.filters:
            result = filter_strategy.filter(result)
        return result

# Enhanced E-commerce Platform
class EcommercePlatform:
    def __init__(self, sorting_strategy: Optional[SortingStrategy] = None,
                 filter_strategy: Optional[FilterStrategy] = None):
        self.products = []
        self.sorting_strategy = sorting_strategy or ComplexSortStrategy('name')
        self.filter_strategy = filter_strategy or CompositeFilter([])
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def set_sorting_strategy(self, strategy: SortingStrategy):
        self.sorting_strategy = strategy
    
    def set_filter_strategy(self, strategy: FilterStrategy):
        self.filter_strategy = strategy
    
    def get_products(self) -> List[Product]:
        filtered_products = self.filter_strategy.filter(self.products)
        return self.sorting_strategy.sort(filtered_products)

# Example usage
def main():
    # Create platform instance
    platform = EcommercePlatform()
    
    # Add sample products
    products = [
        Product("Gaming Laptop", 1299.99, 4.5, "Electronics", "2024-01-15", 5),
        Product("Wireless Mouse", 29.99, 4.8, "Electronics", "2024-01-10", 15),
        Product("Mechanical Keyboard", 89.99, 4.2, "Electronics", "2024-01-20", 0),
        Product("4K Monitor", 399.99, 4.7, "Electronics", "2024-01-05", 3),
        Product("Gaming Chair", 199.99, 4.3, "Furniture", "2024-01-25", 8),
        Product("Desk", 149.99, 4.6, "Furniture", "2024-01-18", 2)
    ]
    
    for product in products:
        platform.add_product(product)
    
    # Example 1: Complex sorting by price (descending) with rating as secondary key
    print("Products sorted by price (desc) and rating:")
    platform.set_sorting_strategy(ComplexSortStrategy('price', 'rating', SortDirection.DESCENDING))
    print(platform.get_products())
    
    # Example 2: Filter by category and price range
    print("\nElectronics products between $30 and $500:")
    composite_filter = CompositeFilter([
        CategoryFilter(["Electronics"]),
        PriceRangeFilter(30, 500)
    ])
    platform.set_filter_strategy(composite_filter)
    print(platform.get_products())
    
    # Example 3: In-stock items sorted by rating
    print("\nIn-stock items sorted by rating:")
    platform.set_filter_strategy(InStockFilter())
    platform.set_sorting_strategy(ComplexSortStrategy('rating', direction=SortDirection.DESCENDING))
    print(platform.get_products())

if __name__ == "__main__":
    main()