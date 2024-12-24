from abc import ABC, abstractmethod

class ATCMediator:
    def __init__(self):
        self.flights = {}
    
    def register_flight(self, flight):
        self.flights[flight.call_sign] = flight
    
    def notify_landing_request(self, sender):
        print(f"\nATC: Processing landing request from {sender.call_sign}")
        # Check other flights and runway status
        for flight in self.flights.values():
            if flight != sender and flight.is_landing:
                print(f"ATC: Denying landing - {flight.call_sign} currently landing")
                return False
        print(f"ATC: Landing approved for {sender.call_sign}")
        return True

class Flight(ABC):
    def __init__(self, atc_mediator, call_sign):
        self.mediator = atc_mediator
        self.call_sign = call_sign
        self.is_landing = False
        self.mediator.register_flight(self)
    
    def request_landing(self):
        print(f"{self.call_sign}: Requesting landing permission")
        if self.mediator.notify_landing_request(self):
            self.is_landing = True
            print(f"{self.call_sign}: Beginning landing sequence")
        else:
            print(f"{self.call_sign}: Holding position")

class CommercialFlight(Flight):
    pass

class CargoFlight(Flight):
    pass

# Usage example
if __name__ == "__main__":
    atc = ATCMediator()
    
    flight1 = CommercialFlight(atc, "AA123")
    flight2 = CargoFlight(atc, "CG456")
    
    flight1.request_landing()
    flight2.request_landing()  # Will be denied while flight1 is landing