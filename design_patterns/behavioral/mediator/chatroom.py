from abc import ABC, abstractmethod

# Mediator Interface
class Mediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: 'User'):
        pass

# Concrete Mediator
class Chatroom(Mediator):
    def __init__(self):
        self.users = []
    
    def register_user(self, user: 'User'):
        self.users.append(user)
    
    def send_message(self, message: str, sender: 'User'):
        for user in self.users:
            if user != sender:
                user.receive_message(message, sender)

# Colleague Interface
class User:
    def __init__(self, name: str, chatroom: Mediator):
        self.name = name
        self.chatroom = chatroom
        self.chatroom.register_user(self)
    
    def send_message(self, message: str):
        print(f"{self.name} sends: {message}")
        self.chatroom.send_message(message, self)
    
    def receive_message(self, message: str, sender: 'User'):
        print(f"{self.name} receives from {sender.name}: {message}")

# Client Code
if __name__ == "__main__":
    chatroom = Chatroom()
    
    alice = User("Alice", chatroom)
    bob = User("Bob", chatroom)
    charlie = User("Charlie", chatroom)
    
    alice.send_message("Hello, everyone!")
    bob.send_message("Hi Alice!")
    charlie.send_message("Good morning!")
