from abc import ABC, abstractmethod


# Component
class Expression(ABC):
    @abstractmethod
    def evaluate(self) -> float:
        pass


# Leaf
class Number(Expression):
    def __init__(self, value: float):
        self.value = value

    def evaluate(self) -> float:
        return self.value


# Composite
class Addition(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self) -> float:
        return self.left.evaluate() + self.right.evaluate()
    
class Multiplication(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def evaluate(self) -> float:
        return self.left.evaluate() * self.right.evaluate()


# Client code
if __name__ == "__main__":
    # Expression: 1 + (2 * 3)
    expr = Addition(Number(1), Multiplication(Number(2), Number(3)))
    
    # Evaluate the expression
    result = expr.evaluate()
    print(f"Result: {result}")


