import random

def simple_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")    
    return wrapper


@simple_decorator
def greet():
    print("Hello World! -- Simple Decorator")


def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling the function: {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result

    return wrapper

@log_decorator
def add(a, b, c=3):
    print(f"Inside add function: a={a}, b={b}, c={c}")
    return a + b + c

def retry_decorator(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed with error: {e}")
        raise Exception("All retries failed")

    return wrapper

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling the function: {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

@retry_decorator
@log_decorator
def make_network_request():
    val = random.random()
    print(f"Making a network request with val = {val}")
    if val < 0.5:
        raise Exception("Network request failed")
    return "Request Successful"


if __name__ == "__main__":
    greet()
    add(1, 2)
    make_network_request()

