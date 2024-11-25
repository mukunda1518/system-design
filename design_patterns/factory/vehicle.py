from abc import ABC, abstractmethod

# Base class for vehicle - Interface

class Vehicle(ABC):
    @abstractmethod
    def get_vehicle_type(self):
        pass

    @abstractmethod
    def get_max_speed(self):
        pass
    
# Concrete implementations for each vehicle

class Car(Vehicle):
    def get_vehicle_type(self):
        return "Car"
    
    def get_max_speed(self):
        return "200 km/h"

class Bike(Vehicle):
    def get_vehicle_type(self):
        return "Bike"
    
    def get_max_speed(self):
        return "100 km/h"

class Truck(Vehicle):
    def get_vehicle_type(self):
        return "Truck"
    
    def get_max_speed(self):
        return "300 km/h"

class Ship(Vehicle):
    def get_vehicle_type(self):
        return "Ship"
    
    def get_max_speed(self):
        return "200 km/h"
    
    
# Create a factory to generate objects of different types

class VehicleFactory:
    
    @staticmethod
    def get_vehicle(vehicle_type) -> Vehicle:
        if vehicle_type == "Car":
            return Car()
        elif vehicle_type == "Bike":
            return Bike()
        elif vehicle_type == "Truck":
            return Truck()
        elif vehicle_type == "Ship":
            return Ship()
        else:
            return ValueError(f"Unknown vehicle type: {vehicle_type}")


# Use the factory to create vehicles
# Client code

if __name__ == "__main__":
    # Vehicle types to create
    vehicle_types = ["Car", "Bike", "Truck", "Ship"]
    
    for vehicle_type in vehicle_types:
        try:
            vehicle = VehicleFactory.get_vehicle(vehicle_type)
            print(f"Vehicle Type: {vehicle.get_vehicle_type()}, Max Speed: {vehicle.get_max_speed()}")
        except ValueError as e:
            print(f"Error: {e}")

