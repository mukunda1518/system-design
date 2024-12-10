from abc import ABC, abstractmethod

# Component
class ArithmeticExpression(ABC):
    @abstractmethod
    def evaluate(self) -> float:
        pass

# Leaf
class Number(ArithmeticExpression):
    def __init__(self, value: float):
        self.value = value

    def evaluate(self) -> float:
        return self.value

# Operation Strategy
class Operation(ABC):
    @abstractmethod
    def compute(self, left: float, right: float) -> float:
        pass

class Addition(Operation):
    def compute(self, left: float, right: float) -> float:
        return left + right

class Subtraction(Operation):
    def compute(self, left: float, right: float) -> float:
        return left - right

class Multiplication(Operation):
    def compute(self, left: float, right: float) -> float:
        return left * right

class Division(Operation):
    def compute(self, left: float, right: float) -> float:
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return left / right

# Composite
class Expression(ArithmeticExpression):
    def __init__(self, left: ArithmeticExpression, right: ArithmeticExpression, operation: Operation):
        self.left = left
        self.right = right
        self.operation = operation

    def evaluate(self) -> float:
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()
        return self.operation.compute(left_value, right_value)

# Client code
if __name__ == "__main__":
    # Expression: (5 + 3) * (2 - 1)
    left_expr = Expression(Number(5), Number(3), Addition())
    right_expr = Expression(Number(2), Number(1), Subtraction())
    full_expr = Expression(left_expr, right_expr, Multiplication())

    # Evaluate the expression
    result = full_expr.evaluate()
    print(f"Result: {result}")
