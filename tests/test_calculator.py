import pytest
from calculator.calculator import Calculator

def test_add():
    assert Calculator.add(2, 3) == 5

def test_subtract():
    assert Calculator.subtract(10, 5) == 5

def test_multiply():
    assert Calculator.multiply(4, 5) == 20

def test_divide():
    assert Calculator.divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(10, 0)

