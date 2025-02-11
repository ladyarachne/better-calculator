"""Calculation module for  single arithmetic operation."""

class Calculation:
    """stores single calculation operation."""

    def __init__(self, operand1: float, operand2: float, operation: str, result: float):
        """initializes  Calculation instance w  operands/ op type/ result."""
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation
        self.result = result

    def to_dict(self):
        """returns calculation as  dictionary."""
        return {
            "operand1": self.operand1,
            "operand2": self.operand2,
            "operation": self.operation,
            "result": self.result
        }

