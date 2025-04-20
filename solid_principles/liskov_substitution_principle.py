

# https://www.enjoyalgorithms.com/blog/liskov-substitution-principle


from abc import ABC, abstractmethod

####  LSP Violation Example

class SuperHero(ABC):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def jump(self):
        pass

    @abstractmethod
    def fly(self):
        pass

class IronMan(SuperHero):
    def attack(self):
        print("IronMan attacks with repulsors!")

    def jump(self):
        print("IronMan jumps with power suit.")

    def fly(self):
        print("IronMan is flying!")

class BabyGroot(SuperHero):
    def attack(self):
        # Groot can't attack!
        pass

    def jump(self):
        print("Baby Groot jumps playfully!")

    def fly(self):
        # Groot can't fly!
        pass

    def heal(self, other):
        other.health = "Healthy"

# --- Code that assumes all SuperHeroes can fly and attack

def battle(hero: SuperHero):
    hero.attack()  # expected to do something
    hero.fly()     # expected to fly

# Using IronMan works fine
battle(IronMan())

# Using BabyGroot causes silent failure or confusion
battle(BabyGroot())  # ❌ LSP violation: behavior is not consistent


# The method battle(hero) relies on the attack() and fly() methods to be meaningful, but BabyGroot does nothing in those methods.
# So although BabyGroot is a subclass, it can’t be safely substituted for the base class — a classic LSP break.

# Use composition over inheritance — define interfaces like CanFly, CanAttack, etc., and only add the behaviors to the heroes that support them.

# --- Interfaces (LSP & ISP) ---

class AttackingBehaviour(ABC):
    @abstractmethod
    def execute(self):
        pass

class MovementBehaviour(ABC):
    @abstractmethod
    def execute(self):
        pass

class HealingBehaviour(ABC):
    @abstractmethod
    def execute(self):
        pass

# --- Concrete Strategies (SRP) ---

# Attacks
class RangedAttack(AttackingBehaviour):
    def execute(self):
        print("Executing Ranged Attack!")

class MeleeAttack(AttackingBehaviour):
    def execute(self):
        print("Executing Melee Attack!")

class NoAttack(AttackingBehaviour):
    def execute(self):
        print("No attack available.")

# Movement
class Fly(MovementBehaviour):
    def execute(self):
        print("Flying!")

class RunFast(MovementBehaviour):
    def execute(self):
        print("Running faster than light!")

class Swing(MovementBehaviour):
    def execute(self):
        print("Swinging through buildings!")

# Healing
class Heal(HealingBehaviour):
    def execute(self):
        print("Healing in progress...")

class NoHealing(HealingBehaviour):
    def execute(self):
        print("Cannot heal.")

# --- SuperHero Base Class (OCP, DIP, LSP) ---

class SuperHero:
    def __init__(self, attack_behavior: AttackingBehaviour,
                       move_behavior: MovementBehaviour,
                       heal_behavior: HealingBehaviour):
        self.attacking_behavior = attack_behavior
        self.movement_behavior = move_behavior
        self.healing_behavior = heal_behavior

    def attack(self):
        self.attacking_behavior.execute()

    def move(self):
        self.movement_behavior.execute()

    def heal(self):
        self.healing_behavior.execute()

# --- Concrete SuperHeroes (LSP) ---

class IronMan(SuperHero):
    def __init__(self):
        super().__init__(RangedAttack(), Fly(), NoHealing())

class BabyGroot(SuperHero):
    def __init__(self):
        super().__init__(NoAttack(), RunFast(), Heal())

class SpiderMan(SuperHero):
    def __init__(self):
        super().__init__(MeleeAttack(), Swing(), NoHealing())

# --- Usage Example ---

if __name__ == "__main__":
    heroes = [
        IronMan(),
        BabyGroot(),
        SpiderMan()
    ]

    for hero in heroes:
        print(f"\n{hero.__class__.__name__} Actions:")
        hero.attack()
        hero.move()
        hero.heal()


# SOLID Breakdown
# SRP: Each class has one responsibility (Attack, Move, Heal).

# OCP: We can add new heroes or new behaviors without modifying existing code.

# LSP: Any subclass of SuperHero can be used interchangeably.

# ISP: Each behavior has its own interface.

# DIP: SuperHero depends on abstractions (*Behaviour), not concrete implementations.