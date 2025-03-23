import logging

class Calculator:
    def perform_operation(self, a: float, operation: str, b: float) -> float:
        logging.info(f"Performing {a} {operation} {b}")
        operations = {
            'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y: x / y if y != 0 else self.handle_divide_by_zero()
        }
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
        return operations[operation](a, b)

    def handle_divide_by_zero(self):
        logging.error("Attempted division by zero")
        raise ZeroDivisionError("Cannot divide by zero.")
