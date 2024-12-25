from abc import ABC, abstractmethod
from typing import List

# Observer interface
class WeatherObserver(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        pass
    
    @abstractmethod
    def unregister_from_subject(self) -> None:
        pass


# Subject interface
class Subject(ABC):
    @abstractmethod
    def register(self, observer: WeatherObserver) -> None:
        pass
    
    @abstractmethod
    def unregister(self, observer: WeatherObserver) -> None:
        pass
    
    @abstractmethod
    def notify(self) -> None:
        pass

# Concrete Subject
class WeatherStation(Subject):
    def __init__(self):
        self._observers: List[WeatherObserver] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0
    
    def register(self, observer: WeatherObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Registered: {observer.__class__.__name__}")
    
    def unregister(self, observer: WeatherObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Unregistered: {observer.__class__.__name__}")
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)
    
    def set_measurements(self, temperature: float, humidity: float, pressure: float) -> None:
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify()

# Concrete Observers
class CurrentConditionsDisplay(WeatherObserver):
    def __init__(self, weather_station: WeatherStation):
        self.weather_station = weather_station
        self.weather_station.register(self)
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        print("\nCurrent Conditions:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
    
    def unregister_from_subject(self) -> None:
        self.weather_station.unregister(self)
        self.weather_station = None  # Remove reference to weather station

class StatisticsDisplay(WeatherObserver):
    def __init__(self, weather_station: WeatherStation):
        self.weather_station = weather_station
        self.weather_station.register(self)
        self.temperatures: List[float] = []
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        self.temperatures.append(temperature)
        avg_temp = sum(self.temperatures) / len(self.temperatures)
        max_temp = max(self.temperatures)
        min_temp = min(self.temperatures)
        
        print("\nTemperature Statistics:")
        print(f"Average: {avg_temp:.1f}°C")
        print(f"Maximum: {max_temp}°C")
        print(f"Minimum: {min_temp}°C")
    
    def unregister_from_subject(self) -> None:
        self.weather_station.unregister(self)
        self.weather_station = None  # Remove reference to weather station

class ForecastDisplay(WeatherObserver):
    def __init__(self, weather_station: WeatherStation):
        self.weather_station = weather_station
        self.weather_station.register(self)
        self.last_pressure = 0.0
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        print("\nWeather Forecast:")
        if pressure > self.last_pressure:
            print("Improving weather on the way!")
        elif pressure < self.last_pressure:
            print("Watch out for cooler, rainy weather")
        else:
            print("More of the same")
        self.last_pressure = pressure
    
    def unregister_from_subject(self) -> None:
        self.weather_station.unregister(self)
        self.weather_station = None  # Remove reference to weather station

# Example usage
def main():
    # Create the WeatherStation (Subject)
    weather_station = WeatherStation()
    
    # Create display elements (Observers)
    current_display = CurrentConditionsDisplay(weather_station)
    statistics_display = StatisticsDisplay(weather_station)
    forecast_display = ForecastDisplay(weather_station)
    
    # Simulate weather changes
    print("\nFirst weather reading:")
    weather_station.set_measurements(25.2, 65.0, 1013.1)
    
    print("\nSecond weather reading:")
    weather_station.set_measurements(26.8, 70.0, 1014.2)
    
    # Unregister the current conditions display
    print("\nUnregistering CurrentConditionsDisplay...")
    current_display.unregister_from_subject()
    
    print("\nThird weather reading (without CurrentConditionsDisplay):")
    weather_station.set_measurements(24.5, 75.0, 1012.8)

if __name__ == "__main__":
    main()