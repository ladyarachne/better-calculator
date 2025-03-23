"""
Tests for the Calculation class.
"""
import pytest
from decimal import Decimal
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

class TestCalculation:
    """Tests for the Calculation class."""
    
    def test_calculation_init(self):
        """Test that a Calculation is initialized correctly."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), add)
        
        # Check that the attributes are set correctly
        assert calc.a == Decimal('10')
        assert calc.b == Decimal('5')
        assert calc.operation == add
    
    def test_calculation_create(self):
        """Test the create static method."""
        # Create a calculation using the create method
        calc = Calculation.create(Decimal('10'), Decimal('5'), add)
        
        # Check that the attributes are set correctly
        assert calc.a == Decimal('10')
        assert calc.b == Decimal('5')
        assert calc.operation == add
    
    def test_calculation_perform_add(self):
        """Test performing an add calculation."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), add)
        
        # Perform the calculation
        result = calc.perform()
        
        # Check the result
        assert result == Decimal('15')
    
    def test_calculation_perform_subtract(self):
        """Test performing a subtract calculation."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), subtract)
        
        # Perform the calculation
        result = calc.perform()
        
        # Check the result
        assert result == Decimal('5')
    
    def test_calculation_perform_multiply(self):
        """Test performing a multiply calculation."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), multiply)
        
        # Perform the calculation
        result = calc.perform()
        
        # Check the result
        assert result == Decimal('50')
    
    def test_calculation_perform_divide(self):
        """Test performing a divide calculation."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), divide)
        
        # Perform the calculation
        result = calc.perform()
        
        # Check the result
        assert result == Decimal('2')
    
    def test_calculation_perform_divide_by_zero(self):
        """Test that dividing by zero raises a ValueError."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('0'), divide)
        
        # Perform the calculation and check that it raises a ValueError
        with pytest.raises(ValueError):
            calc.perform()
    
    def test_calculation_repr(self):
        """Test the __repr__ method."""
        # Create a calculation
        calc = Calculation(Decimal('10'), Decimal('5'), add)
        
        # Check the string representation
        assert repr(calc) == "Calculation(10, 5, add)"
