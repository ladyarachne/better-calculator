"""
Tests for the calculation history module.
"""
import os
import pytest
import pandas as pd
from decimal import Decimal

from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.calculation_history import get_history_facade

@pytest.fixture
def history_facade():
    """Fixture to provide a clean history facade for each test."""
    facade = get_history_facade()
    facade.clear_history()
    return facade

@pytest.fixture
def sample_calculation():
    """Fixture to provide a sample calculation."""
    return Calculation(Decimal('10'), Decimal('5'), add)

def test_add_calculation(history_facade, sample_calculation):
    """Test adding a calculation to history."""
    result = history_facade.add_calculation(sample_calculation)
    assert result == Decimal('15')
    
    history = history_facade.get_history()
    assert len(history) == 1
    assert history.iloc[0]['operation'] == 'add'
    assert history.iloc[0]['a'] == 10.0
    assert history.iloc[0]['b'] == 5.0
    assert history.iloc[0]['result'] == 15.0

def test_clear_history(history_facade, sample_calculation):
    """Test clearing the history."""
    history_facade.add_calculation(sample_calculation)
    assert len(history_facade.get_history()) == 1
    
    history_facade.clear_history()
    assert len(history_facade.get_history()) == 0

def test_get_history_as_dict(history_facade, sample_calculation):
    """Test getting history as a dictionary."""
    history_facade.add_calculation(sample_calculation)
    history_dict = history_facade.get_history_as_dict()
    
    assert len(history_dict) == 1
    assert history_dict[0]['operation'] == 'add'
    assert history_dict[0]['a'] == 10.0
    assert history_dict[0]['b'] == 5.0
    assert history_dict[0]['result'] == 15.0

def test_save_and_load_history(history_facade, sample_calculation, tmp_path):
    """Test saving and loading history to/from a file."""
    # Add a calculation and save to a temporary file
    history_facade.add_calculation(sample_calculation)
    test_file = tmp_path / "test_history.csv"
    history_facade.save_history(str(test_file))
    
    # Clear history and verify it's empty
    history_facade.clear_history()
    assert len(history_facade.get_history()) == 0
    
    # Load history from file and verify it's restored
    history_facade.load_history(str(test_file))
    history = history_facade.get_history()
    assert len(history) == 1
    assert history.iloc[0]['operation'] == 'add'
    assert history.iloc[0]['result'] == 15.0

def test_delete_history_file(history_facade, sample_calculation, tmp_path):
    """Test deleting a history file."""
    # Add a calculation and save to a temporary file
    history_facade.add_calculation(sample_calculation)
    test_file = tmp_path / "test_history.csv"
    history_facade.save_history(str(test_file))
    
    # Verify file exists
    assert os.path.exists(test_file)
    
    # Delete file and verify it's gone
    history_facade.delete_history_file(str(test_file))
    assert not os.path.exists(test_file)

def test_filter_by_operation(history_facade):
    """Test filtering history by operation."""
    # Add different types of calculations
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), subtract))
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), multiply))
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))
    
    # Filter by add operation
    filtered = history_facade.filter_by_operation('add')
    assert len(filtered) == 2
    assert all(op == 'add' for op in filtered['operation'])
    
    # Filter by subtract operation
    filtered = history_facade.filter_by_operation('subtract')
    assert len(filtered) == 1
    assert filtered.iloc[0]['operation'] == 'subtract'

def test_get_statistics(history_facade):
    """Test getting statistics about the history."""
    # Add different calculations
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), add))  # 15
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), subtract))  # 5
    history_facade.add_calculation(Calculation(Decimal('10'), Decimal('5'), multiply))  # 50
    
    stats = history_facade.get_statistics()
    assert stats['count'] == 3
    assert stats['operations']['add'] == 1
    assert stats['operations']['subtract'] == 1
    assert stats['operations']['multiply'] == 1
    assert stats['avg_result'] == (15 + 5 + 50) / 3
    assert stats['min_result'] == 5
    assert stats['max_result'] == 50

def test_empty_statistics(history_facade):
    """Test getting statistics with empty history."""
    stats = history_facade.get_statistics()
    assert stats['count'] == 0
