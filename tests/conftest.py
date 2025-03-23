"""
Pytest configuration file.
Provides fixtures that can be used across all tests.
"""
import os
import pytest
from decimal import Decimal
from unittest.mock import patch

from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.calculation_history import get_history_facade
from calculator.plugins import get_plugin_manager
from calculator.logger import LoggerSingleton, get_logger

@pytest.fixture
def reset_singletons():
    """Reset all singleton instances before each test."""
    # Reset the LoggerSingleton
    LoggerSingleton._instance = None
    
    # Reset the CalculationHistoryFacade
    history_facade = get_history_facade()
    history_facade.clear_history()
    
    # Reset the PluginManager
    plugin_manager = get_plugin_manager()
    plugin_manager._plugins = {}
    
    yield

@pytest.fixture
def sample_calculations():
    """Provide a list of sample calculations."""
    return [
        Calculation(Decimal('10'), Decimal('5'), add),
        Calculation(Decimal('20'), Decimal('10'), subtract),
        Calculation(Decimal('4'), Decimal('5'), multiply),
        Calculation(Decimal('20'), Decimal('4'), divide)
    ]

@pytest.fixture
def clean_env():
    """Provide a clean environment with no calculator-specific variables."""
    # Save the original environment
    original_env = os.environ.copy()
    
    # Remove calculator-specific variables
    for var in list(os.environ.keys()):
        if var.startswith('CALCULATOR_'):
            del os.environ[var]
    
    yield
    
    # Restore the original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def logger():
    """Provide a logger instance."""
    # Reset the singleton to ensure a clean state
    LoggerSingleton._instance = None
    return get_logger()

@pytest.fixture
def history_facade():
    """Provide a history facade instance with a clean history."""
    facade = get_history_facade()
    facade.clear_history()
    return facade

@pytest.fixture
def plugin_manager():
    """Provide a plugin manager instance with no plugins loaded."""
    manager = get_plugin_manager()
    manager._plugins = {}
    return manager
