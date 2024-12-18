
# Scenario: A Proxy for Expensive Object Initialization

# Imagine a scenario where creating a large dataset is an expensive operation, and we want to delay its initialization until it is actually needed

from time import sleep


# Subject Interface
class Dataset:
    def load_data(self):
        raise NotImplementedError


# Real Subject
class ExpensiveDataset(Dataset):
    def __init__(self):
        print("ExpensiveDataset: Initializing large dataset...")
        sleep(2)    # Simulating a costly operation
        self.data = [x for x in range(1, 10001)]  # Large dataset
        print("ExpensiveDataset: Dataset ready!")
    
    def load_data(self):
        return self.data


# Proxy
class DatasetProxy(Dataset):
    def __init__(self):
        self._dataset = None

    def load_data(self):
        if self._dataset is None:
            print("DatasetProxy: Loading dataset for the first time...")
            self._dataset = ExpensiveDataset()  # Lazy initialization
        else:
            print("DatasetProxy: Using cached dataset...")
        return self._dataset.load_data()
        


# Scenario: Access Control with Proxy

# Real Subject
class SecureDatabase:
    def __init__(self):
        self.data = {"secret_key": "12345", "confidential_info": "Sensitive Data"}

    def read_data(self):
        return self.data

# Proxy
class DatabaseProxy:
    def __init__(self, user_role):
        self._user_role = user_role
        self._database = SecureDatabase()  # Real Subject

    def read_data(self):
        if self._user_role == "admin":
            print("DatabaseProxy: Access granted to admin.")
            return self._database.read_data()
        else:
            raise PermissionError("DatabaseProxy: Access denied. Admin role required.")


# Scenario: Remote Proxy (Simulating Remote Method Invocation)

# Problem
# A remote server provides a service to calculate factorials, but the client should not deal with the actual network communication logic.
# A Proxy class will handle this, making the client think it's interacting with a local object.

import time
import random

# Real Subject
class RemoteFactorialService:
    def calculate_factorial(self, number):
        print(f"RemoteFactorialService: Calculating factorial for {number} on a remote server...")
        time.sleep(2)  # Simulating network delay
        result = 1
        for i in range(1, number + 1):
            result *= i
        return result

# Proxy
class FactorialProxy:
    def __init__(self):
        self._service = RemoteFactorialService()
        self._cache = {}  # Cache results for efficiency

    def calculate_factorial(self, number):
        if number in self._cache:
            print(f"FactorialProxy: Returning cached result for {number}")
            return self._cache[number]
        
        print(f"FactorialProxy: Sending request to remote server for {number}")
        result = self._service.calculate_factorial(number)
        self._cache[number] = result
        return result



# Client Code
if __name__ == "__main__":
    print("Client: Creating proxy...")
    dataset_proxy = DatasetProxy()
    print("\nClient: Accessing data for the first time...")
    data = dataset_proxy.load_data()
    print(f"Data loaded: {data[:5]}... (showing first 5 entries)")

    print("\nClient: Accessing data again...")
    data = dataset_proxy.load_data()
    print(f"Data loaded: {data[:5]}... (showing first 5 entries)")
    


    print("Client: Trying to access the database as a 'user'...")
    user_proxy = DatabaseProxy(user_role="user")
    try:
        print(user_proxy.read_data())
    except PermissionError as e:
        print(e)

    print("\nClient: Trying to access the database as an 'admin'...")
    admin_proxy = DatabaseProxy(user_role="admin")
    try:
        print(admin_proxy.read_data())
    except PermissionError as e:
        print(e)


    proxy = FactorialProxy()
    # Simulate multiple client requests
    numbers = [random.randint(1, 5) for _ in range(3)]
    for num in numbers:
        print(f"\nClient: Requesting factorial for {num}")
        result = proxy.calculate_factorial(num)
        print(f"Result: {num}! = {result}")

    # Re-request to demonstrate caching
    print(f"\nClient: Requesting factorial for {numbers[0]} again")
    result = proxy.calculate_factorial(numbers[0])
    print(f"Result: {numbers[0]}! = {result}")







