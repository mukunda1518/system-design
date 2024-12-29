import datetime
import uuid
import time
import random

from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional, List


class VehicleType(Enum):
    CAR = "Car"
    TRUCK = "Truck"
    MOTORCYCLE = "Motorcycle"
    VAN = "Van"

class ParkingSpotType(Enum):
    COMPACT = "Compact"
    LARGE = "Large"
    MOTORCYCLE = "Motorcycle"

class PaymentType(Enum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    UPI = "UPI"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

# Abstract base class
class Vehicle(ABC):
    def __init__(self, registration_number: str):
        self.registration_number = registration_number

    @abstractmethod
    def get_vehicle_type(self) -> VehicleType:
        pass

# Vehicle Implementations
class Car(Vehicle):
    def get_vehicle_type(self) -> VehicleType:
        return VehicleType.CAR

class Truck(Vehicle):
    def get_vehicle_type(self) -> VehicleType:
        return VehicleType.TRUCK

class Motorcycle(Vehicle):
    def get_vehicle_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE

class Van(Vehicle):
    def get_vehicle_type(self) -> VehicleType:
        return VehicleType.VAN


# Abstract base class
class ParkingSpot(ABC):
    def __init__(self, spot_id: str, floor_id: str):
        self.spot_id = spot_id
        self.floor_id = floor_id
        self.is_free: bool = True
        self.is_reserved: bool = False
        self.vehicle: Optional[Vehicle] = None

    @abstractmethod
    def get_parking_spot_type(self) -> ParkingSpotType:
        pass

    def can_park_vehicle(self, vehicle: Vehicle) -> bool:
        if not self.is_free or self.is_reserved:
            return False
        return self._vehicle_can_fit(vehicle)

    @abstractmethod
    def _vehicle_can_fit(self, vehicle: Vehicle) -> bool:
        pass

    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        if self.can_park_vehicle(vehicle):
            self.vehicle = vehicle
            self.is_free = False
            self.is_reserved = True
            return True
        return False

    def remove_vehicle(self) -> bool:
        if not self.is_free:
            self.vehicle = None
            self.is_free = True
            self.is_reserved = False
            return True
        return False

# Parking Spot Implementation
class CompactSpot(ParkingSpot):
    def get_parking_spot_type(self) -> ParkingSpotType:
        return ParkingSpotType.COMPACT

    def _vehicle_can_fit(self, vehicle: Vehicle) -> bool:
        return vehicle.get_vehicle_type() in [VehicleType.CAR]

class LargeSpot(ParkingSpot):
    def get_parking_spot_type(self) -> ParkingSpotType:
        return ParkingSpotType.LARGE

    def _vehicle_can_fit(self, vehicle: Vehicle) -> bool:
        return vehicle.get_vehicle_type() in [VehicleType.TRUCK, VehicleType.VAN]

class MotorCycleSpot(ParkingSpot):
    def get_parking_spot_type(self) -> ParkingSpotType:
        return ParkingSpotType.MOTORCYCLE

    def _vehicle_can_fit(self, vehicle: Vehicle) -> bool:
        return vehicle.get_vehicle_type() in [VehicleType.MOTORCYCLE]

# Observer Pattern for Display Board
class ParkingLotObserver(ABC):
    @abstractmethod
    def update(self, floor_id: str, parking_spots: dict[ParkingSpotType, list[ParkingSpot]]):
        pass

class DisplayBoard(ParkingLotObserver):
    def __init__(self, floor_id: str):
        self.floor_id = floor_id
        self.current_status = {}

    def update(self, parking_spots: dict[ParkingSpotType, list[ParkingSpot]]) -> dict:
        floor_status = {
            "floor_id": self.floor_id,
            "spots": {}
        }
        for spot_type, spots in parking_spots.items():
            free_count = sum(1 for spot in spots if spot.is_free and not spot.is_reserved)
            total_count = len(spots)
            floor_status["spots"][spot_type.value] = {
                "free": free_count,
                "total": total_count,
                "occupied": total_count - free_count
            }
        self.current_status = floor_status

    def get_display_status(self, parking_spots: dict[ParkingSpotType, list[ParkingSpot]]) -> dict:
        floor_status = {
            "floor_id": self.floor_id,
            "spots": {}
        }
        for spot_type, spots in parking_spots.items():
            free_count = sum(1 for spot in spots if spot.is_free and not spot.is_reserved)
            total_count = len(spots)
            floor_status["spots"][spot_type.value] = {
                "free": free_count,
                "total": total_count,
                "occupied": total_count - free_count
            }
        return floor_status

class ParkingFloor(ABC):
    def __init__(self, floor_id: str):
        self.floor_id = floor_id
        self.parking_spots: dict[ParkingSpotType, list[ParkingSpot]] = {
            spot_type: [] for spot_type in ParkingSpotType
        }
        self.display_board = DisplayBoard(floor_id)
        self.observers: List[ParkingLotObserver] = [self.display_board]
        self.is_full = False

    def add_observer(self, observer: ParkingLotObserver):
        self.observers.append(observer)

    def remove_observer(self, observer: ParkingLotObserver):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.floor_id, self.parking_spots)

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        vehicle_type = vehicle.get_vehicle_type()
        compatible_spot_types = self._get_compatible_spot_types(vehicle_type)
        for spot_type in compatible_spot_types:
            for spot in self.parking_spots[spot_type]:
                if spot.can_park_vehicle(vehicle):
                    return spot
        return None

    def _get_compatible_spot_types(self, vehicle_type: VehicleType) -> list[ParkingSpotType]:
        compatibility_map = {
            VehicleType.MOTORCYCLE: [ParkingSpotType.MOTORCYCLE],
            VehicleType.CAR: [ParkingSpotType.COMPACT],
            VehicleType.VAN: [ParkingSpotType.LARGE],
            VehicleType.TRUCK: [ParkingSpotType.LARGE]
        }
        return compatibility_map.get(vehicle_type, [])

    def add_parking_spot(self, spot: ParkingSpot):
        spot_type = spot.get_parking_spot_type()
        self.parking_spots[spot_type].append(spot)

    def get_parking_spots_status(self):
        return self.display_board.get_display_status(self.parking_spots)


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass
    
class CashPayment(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Simulate cash payment processing
        print(f"Processing cash payment of ${amount}")
        return True

class CreditCardPayment(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Simulate credit card payment processing
        print(f"Processing credit card payment of ${amount}")
        return True

class DebitCardPayment(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Simulate debit card payment processing
        print(f"Processing debit card payment of ${amount}")
        return True

class UPIPayment(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Simulate UPI payment processing
        print(f"Processing UPI payment of ${amount}")
        return True

class Payment:
    def __init__(self, amount: float, payment_strategy: PaymentStrategy):
        self.payment_id = str(uuid.uuid4())
        self.amount = amount
        self.payment_strategy = payment_strategy
        self.payment_status = PaymentStatus.PENDING
        self.processed_at: Optional[datetime.datetime] = None

    def process_payment(self) -> bool:
        if self.payment_strategy.process_payment(self.amount):
            self.payment_status = PaymentStatus.COMPLETED
            self.processed_at = datetime.datetime.now()
            return True
        self.payment_status = PaymentStatus.FAILED
        return False



class ParkingTicket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.datetime.now()
        self.exit_time: Optional[datetime.datetime] = None
        self.payment: Optional[Payment] = None
        self.is_paid = False

    def calculate_fee(self, hourly_rate: float) -> float:
        if not self.exit_time:
            self.exit_time = datetime.datetime.now()
        
        duration = (self.exit_time - self.entry_time).total_seconds() / 3600  # hours
        return round(duration * hourly_rate, 2)

class EntryPanel:
    def __init__(self, panel_id: str):
        self.panel_id = panel_id

    def issue_ticket(self, vehicle: Vehicle, spot: ParkingSpot) -> ParkingTicket:
        vehicle_assigned = spot.assign_vehicle(vehicle)
        if vehicle_assigned:
            return ParkingTicket(vehicle, spot)
        return None

class ExitPanel:
    def __init__(self, panel_id: str):
        self.panel_id = panel_id
    
    def process_exit(self, ticket: ParkingTicket, payment_strategy: PaymentStrategy) -> bool:
        if not ticket.is_paid:
            fee = self._calculate_parking_fee(ticket)
            payment = Payment(fee, payment_strategy)
            if payment.process_payment():
                ticket.payment = payment
                ticket.is_paid = True
                ticket.spot.remove_vehicle()
                return True
        return False
    
    def _calculate_parking_fee(self, ticket: ParkingTicket) -> float:
        spot = ticket.spot
        hourly_cost = HourlyCost().get_cost(spot_type=spot.get_parking_spot_type())
        fee = ticket.calculate_fee(hourly_cost)
        return fee

class HourlyCost:
    def __init__(self):
        self.hourly_cost: dict[ParkingSpotType, float] = {
            ParkingSpotType.MOTORCYCLE: 10.0,
            ParkingSpotType.COMPACT: 20.0,
            ParkingSpotType.LARGE: 30.0,
        }

    def get_cost(self, spot_type: ParkingSpotType) -> float:
        return self.hourly_cost[spot_type]
         
class ParkingLot:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.floors: list[ParkingFloor] = []
        self.entry_panels: list[EntryPanel] = []
        self.exit_panels: list[ExitPanel] = []
        self.tickets: dict[str, ParkingTicket] = {}

    def add_floor(self, floor: ParkingFloor) -> None:
        self.floors.append(floor)

    def add_entry_panel(self, panel: EntryPanel) -> None:
        self.entry_panels.append(panel)

    def add_exit_panel(self, panel: ExitPanel) -> None:
        self.exit_panels.append(panel)

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for floor in self.floors:
            spot = floor.find_available_spot(vehicle)
            if spot:
                return spot
        return None

    def issue_ticket(self, vehicle: Vehicle, entry_panel_id: str) -> Optional[ParkingTicket]:
        entry_panel = next((panel for panel in self.entry_panels if panel.panel_id == entry_panel_id), None)
        if not entry_panel:
            return None

        spot = self.find_available_spot(vehicle)
        if spot:
            return entry_panel.issue_ticket(vehicle, spot)
        return None

    def process_exit(self, ticket_id: str, exit_panel_id: str, payment_type: PaymentType) -> bool:
        exit_panel = next((panel for panel in self.exit_panels if panel.panel_id == exit_panel_id), None)
        if not exit_panel:
            return None
        
        ticket = self.tickets[ticket_id]
        return exit_panel.process_exit(ticket, payment_type)
            
    def get_parking_lot_status(self) -> dict:
        return {
            floor.floor_id: floor.get_parking_spots_status()
            for floor in self.floors
        }



### Client Code

class ParkingSpotFactory:
    def create_spot(self, spot_type: ParkingSpotType, spot_id: str, floor_id: str) -> ParkingSpot:
        if spot_type == ParkingSpotType.MOTORCYCLE:
            spot = MotorCycleSpot(spot_id, floor_id)
        elif spot_type == ParkingSpotType.COMPACT:
            spot = CompactSpot(spot_id, floor_id)
        elif spot_type == ParkingSpotType.LARGE:
            spot = LargeSpot(spot_id, floor_id)
        else:
            print("Invalid spot type")
            spot = None
        return spot

class PaymentFactory:
    def create_payment(self, payment_type: PaymentType) -> Payment:
        if payment_type == PaymentType.CREDIT_CARD:
            payment = CreditCardPayment()
        elif payment_type == PaymentType.DEBIT_CARD:
            payment = DebitCardPayment()
        elif payment_type == PaymentType.CASH:
            payment = CashPayment()
        elif payment_type == PaymentType.UPI:
            payment = UPIPayment()
        else:
            print("Invalid payment type")
            payment = None
        return payment

def setup_parking_lot() -> ParkingLot:
    parking_lot = ParkingLot()

    # Add entry and exit panels
    for i in range(2):
        entry_panel = EntryPanel(f"ENTRY-{i+1}")
        exit_panel = ExitPanel(f"EXIT-{i+1}")
        parking_lot.add_entry_panel(entry_panel)
        parking_lot.add_exit_panel(exit_panel)

    # Create floors
    for floor_num in range(3):
        floor = ParkingFloor(f"Floor-{floor_num + 1}")

        # Add different types of spots to each floor
        spot_distribution = {
            ParkingSpotType.COMPACT: 2,
            ParkingSpotType.LARGE: 2,
            ParkingSpotType.MOTORCYCLE: 2
        }
        for spot_type, count in spot_distribution.items():
            for i in range(count):
                spot_id = f"{floor.floor_id}-{spot_type.value}-{i+1}"
                spot = ParkingSpotFactory().create_spot(spot_type, spot_id, floor.floor_id)
                floor.add_parking_spot(spot)
        parking_lot.add_floor(floor)

    return parking_lot


def simulate_parking_scenario():
    parking_lot = setup_parking_lot()
    issued_tickets = []
    
    # Create various vehicles
    vehicles = [
        Car("Car-001"),
        Car("Car-002"),
        Motorcycle("Moto-001"),
        Motorcycle("Moto-002"),
        Truck("Truck-001"),
        Van("Van-001"),
        Truck("Truck-002"),
        Van("Van-002"),
        Truck("Truck-001"),
        Van("Van-001"),
        Truck("Truck-002"),
        Van("Van-002"),
    ]

    print("\nInitial Parking Lot Status")
    print("-" * 50)
    print(parking_lot.get_parking_lot_status())

    # Simulate parking for each vehicle
    print("\nParking Vehicles")
    print("-" * 50)
    for vehicle in vehicles:
        try:
            ticket = parking_lot.issue_ticket(vehicle, "ENTRY-1")
            if ticket:
                parking_lot.tickets[ticket.ticket_id] = ticket  # Store ticket in parking lot
                issued_tickets.append(ticket)
                print(f"✅ Parked {vehicle.get_vehicle_type().value} - ({vehicle.registration_number})")
                print(f"   Ticket ID: {ticket.ticket_id}")
                print(f"   Spot ID: {ticket.spot.spot_id}")
            else:
                print(f"❌ No parking space available for {vehicle.get_vehicle_type().value} - ({vehicle.registration_number})")
        except Exception as e:
            print(f"Error while parking vehicle: {str(e)}")
    
    print("\nParking Lot Status After Parking:")
    print("-" * 50)
    print(parking_lot.get_parking_lot_status())

    # Simulate exit for some vehicles with different payment types
    print("\nProcessing Exits")
    print("-" * 50)

    # Wait for some time to simulate parking duration
    time.sleep(2)  # Simulate 2 seconds of parking time
    
    for ticket in issued_tickets[:3]:  # Process exit for first 3 vehicles
        payment_type = random.choice(list(PaymentType))
        payment_strategy = PaymentFactory().create_payment(payment_type)
        try:
            success = parking_lot.exit_panels[0].process_exit(ticket, payment_strategy)
            if success:
                print(f"✅ Exit processed for vehicle {ticket.vehicle.registration_number}")
                print(f"   Payment Type: {payment_type.value}")
                print(f"   Amount Paid: ${ticket.payment.amount}")
                print(f"   Parking Duration: {format_duration(ticket.entry_time, ticket.exit_time)}")
            else:
                print(f"❌ Exit failed for vehicle {ticket.vehicle.registration_number}")
        except Exception as e:
            print(f"Error processing exit: {str(e)}")
            
    print("\nFinal Parking Lot Status:")
    print("-" * 50)
    print(parking_lot.get_parking_lot_status())

def format_duration(entry_time, exit_time):
    """Format the parking duration in a readable format"""
    duration = exit_time - entry_time
    hours = duration.total_seconds() / 3600
    return f"{hours:.2f} hours"

if __name__ == "__main__":
    simulate_parking_scenario()

