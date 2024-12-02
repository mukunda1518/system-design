

class Logger:
    _instance = None    # Class attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance of Logger is created
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'log_file'):
            self.log_file = 'log.txt'
            self.logs = []      # In-memory log storage for simplicity

    def log(self, message):
        # Append a message to the logs
        self.logs.append(message)
        with open(self.log_file, 'a') as file:
            file.write(message + '\n')

    def get_logs(self):
        return self.logs


logger1 = Logger()
logger1.log("First log message")

logger2 = Logger()
logger2.log("Second Log message")


# Confirm logger1 and logger2 are the same instance
print(logger1 is logger2)

# Both logger1 and logger2 share the same log file and log data
print(logger1.get_logs())
