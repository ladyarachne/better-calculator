"""calculator."""

class Calculator:
    """calculator class"""

    @staticmethod
    def add(a: float, b: float) -> float:
        """Returns the sum of two numbers."""
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """returns difference"""
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """returns product"""
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """returns quotient, raises ZeroDivisionError if necessary"""
        if b == 0:
            raise ZeroDivisionError("no zero division")
        return a / b
