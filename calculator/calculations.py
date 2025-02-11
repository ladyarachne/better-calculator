"""Calculations history"""

class Calculations:
    """manages history of calculations"""

    history = []

    @classmethod
    def add_calculation(cls, calculation):
        """adds calculation instance to history"""
        cls.history.append(calculation)

    @classmethod
    def get_last_calculation(cls):
        """retrieves last calculation from history/ None if history is empty"""
        return cls.history[-1] if cls.history else None

    @classmethod
    def clear_history(cls):
        """clears history."""
        cls.history.clear()
