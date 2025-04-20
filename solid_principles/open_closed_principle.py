# https://www.enjoyalgorithms.com/blog/open-close-principle


# Violation of Open/Closed Principle

# Every time you add a new character (like Yoshi or Bowser), you modify both attack() and jump() functions.

# This breaks the Open/Closed Principle, which says:

# "Software entities should be open for extension, but closed for modification."


def attack(character):
    if character.name == 'Mario':
        # logic for Mario attack
        pass
    elif character.name == 'Luigi':
        # logic for Luigi attack
        pass

def jump(character):
    if character.name == 'Mario':
        # logic for Mario jump
        pass
    elif character.name == 'Luigi':
        # logic for Luigi jump
        pass



# Achieved through abstraction (e.g., interfaces, abstract classes) and inheritance

from abc import ABC, abstractmethod

class Character(ABC):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def jump(self):
        pass

class Mario(Character):
    def attack(self):
        print("Mario uses fireball!")

    def jump(self):
        print("Mario jumps high!")

class Luigi(Character):
    def attack(self):
        print("Luigi uses vacuum!")

    def jump(self):
        print("Luigi jumps stylishly!")

# Now the client code can work with any Character without modification
def game_actions(character: Character):
    character.attack()
    character.jump()

# Usage
mario = Mario()
luigi = Luigi()

game_actions(mario)
game_actions(luigi)

