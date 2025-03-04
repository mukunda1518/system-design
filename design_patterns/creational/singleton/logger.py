# https://medium.com/@minuray10/singleton-design-pattern-in-python-47d90fd27365

import threading

class Logger:
    _instance = None    # Class attribute to hold the single instance
    _lock = threading.Lock() # Lock to synchronize instance creation

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance of Logger is created
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    if not hasattr(cls._instance, 'log_file'):
                        cls._instance.log_file = "log.txt"
                        cls._instance.logs = []
        return cls._instance
            
    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance
        

    def log(self, message):
        # Append a message to the logs
        self.logs.append(message)
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')

    def get_logs(self):
        return self.logs


logger1 = Logger.get_instance()
logger1.log("First log message")

logger2 = Logger.get_instance()
logger2.log("Second Log message")


# Confirm logger1 and logger2 are the same instance
print(logger1 is logger2)
print(id(logger1))
print(id(logger2))
# Both logger1 and logger2 share the same log file and log data
print(logger1.get_logs())
