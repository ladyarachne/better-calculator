"""
Tests for the Calculations class.
"""
import pytest
from decimal import Decimal
from calculator.calculation import Calculation
from calculator.calculations import Calculations
from calculator.operations import add, subtract, multiply, divide

class TestCalculations:
    """Tests for the Calculations class."""
    
    @pytest.fixture
    def setup_calculations(self):
        """Fixture to set up and clean up the Calculations class."""
        # Clear the history before each test
        Calculations.clear_history()
        
        # Add some calculations to the history
        Calculations.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
        Calculations.add_calculation(Calculation(Decimal('20'), Decimal('10'), subtract))
        Calculations.add_calculation(Calculation(Decimal('4'), Decimal('5'), multiply))
        
        yield
        
        # Clear the history after each test
        Calculations.clear_history()
    
    def test_add_calculation(self):
        """Test adding a calculation to the history."""
        # Clear the history
        Calculations.clear_history()
        
        # Add a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), add)
        Calculations.add_calculation(calc)
        
        # Check that the calculation was added
        history = Calculations.get_history()
        assert len(history) == 1
        assert history[0] == calc
    
    def test_get_history(self, setup_calculations):
        """Test getting the history."""
        # Get the history
        history = Calculations.get_history()
        
        # Check that the history has the expected number of calculations
        assert len(history) == 3
        
        # Check that the calculations are in the correct order
        assert history[0].operation == add
        assert history[1].operation == subtract
        assert history[2].operation == multiply
    
    def test_clear_history(self, setup_calculations):
        """Test clearing the history."""
        # Check that the history has calculations
        assert len(Calculations.get_history()) == 3
        
        # Clear the history
        Calculations.clear_history()
        
        # Check that the history is empty
        assert len(Calculations.get_history()) == 0
    
    def test_get_latest(self, setup_calculations):
        """Test getting the latest calculation."""
        # Get the latest calculation
        latest = Calculations.get_latest()
        
        # Check that it's the correct calculation
        assert latest.operation == multiply
        assert latest.a == Decimal('4')
        assert latest.b == Decimal('5')
    
    def test_get_latest_empty(self):
        """Test getting the latest calculation when history is empty."""
        # Clear the history
        Calculations.clear_history()
        
        # Get the latest calculation
        latest = Calculations.get_latest()
        
        # Check that it's None
        assert latest is None
    
    def test_find_by_operation(self, setup_calculations):
        """Test finding calculations by operation."""
        # Find calculations with the add operation
        add_calcs = Calculations.find_by_operation('add')
        
        # Check that the correct calculations were found
        assert len(add_calcs) == 1
        assert add_calcs[0].operation == add
        
        # Find calculations with the subtract operation
        subtract_calcs = Calculations.find_by_operation('subtract')
        
        # Check that the correct calculations were found
        assert len(subtract_calcs) == 1
        assert subtract_calcs[0].operation == subtract
        
        # Find calculations with a non-existent operation
        nonexistent_calcs = Calculations.find_by_operation('nonexistent')
        
        # Check that no calculations were found
        assert len(nonexistent_calcs) == 0
