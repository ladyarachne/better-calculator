"""
Tests for the plugin system.
"""
import os
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from calculator.plugins import PluginInterface, get_plugin_manager
from calculator.plugins.sample_plugin import SquareRootPlugin, PowerPlugin, StatisticsPlugin

class TestPluginInterface:
    """Tests for the PluginInterface class."""
    
    def test_plugin_interface_abstract(self):
        """Test that PluginInterface methods raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            PluginInterface.get_command()
        
        with pytest.raises(NotImplementedError):
            PluginInterface.get_description()
        
        with pytest.raises(NotImplementedError):
            PluginInterface.execute()

class TestPluginManager:
    """Tests for the PluginManager class."""
    
    @pytest.fixture
    def plugin_manager(self):
        """Fixture to provide a clean plugin manager for each test."""
        manager = get_plugin_manager()
        # Reset the plugins dictionary to ensure a clean state
        manager._plugins = {}
        return manager
    
    def test_singleton_pattern(self):
        """Test that PluginManager follows the Singleton pattern."""
        manager1 = get_plugin_manager()
        manager2 = get_plugin_manager()
        assert manager1 is manager2
    
    def test_load_plugins(self, plugin_manager):
        """Test loading plugins from the plugins package."""
        # Load plugins
        plugin_manager.load_plugins()
        
        # Check that plugins were loaded
        assert len(plugin_manager.get_plugin_commands()) > 0
        assert "sqrt" in plugin_manager.get_plugin_commands()
        assert "power" in plugin_manager.get_plugin_commands()
        assert "stats" in plugin_manager.get_plugin_commands()
    
    def test_get_plugin(self, plugin_manager):
        """Test getting a plugin by command name."""
        # Load plugins
        plugin_manager.load_plugins()
        
        # Get plugins
        sqrt_plugin = plugin_manager.get_plugin("sqrt")
        power_plugin = plugin_manager.get_plugin("power")
        
        # Check that the correct plugins were returned
        assert sqrt_plugin is SquareRootPlugin
        assert power_plugin is PowerPlugin
        
        # Check that non-existent plugin returns None
        assert plugin_manager.get_plugin("nonexistent") is None
    
    def test_get_plugin_descriptions(self, plugin_manager):
        """Test getting plugin descriptions."""
        # Load plugins
        plugin_manager.load_plugins()
        
        # Get descriptions
        descriptions = plugin_manager.get_plugin_descriptions()
        
        # Check that descriptions were returned
        assert "sqrt" in descriptions
        assert descriptions["sqrt"] == "Calculate the square root of a number"
        assert "power" in descriptions
        assert descriptions["power"] == "Calculate a number raised to a power"
    
    def test_execute_plugin(self, plugin_manager):
        """Test executing a plugin."""
        # Load plugins
        plugin_manager.load_plugins()
        
        # Execute plugins
        sqrt_result = plugin_manager.execute_plugin("sqrt", "16")
        power_result = plugin_manager.execute_plugin("power", "2", "3")
        
        # Check results
        assert sqrt_result == Decimal('4')
        assert power_result == Decimal('8')
        
        # Check that executing a non-existent plugin raises ValueError
        with pytest.raises(ValueError):
            plugin_manager.execute_plugin("nonexistent")

class TestSamplePlugins:
    """Tests for the sample plugins."""
    
    def test_square_root_plugin(self):
        """Test the SquareRootPlugin."""
        # Test get_command and get_description
        assert SquareRootPlugin.get_command() == "sqrt"
        assert SquareRootPlugin.get_description() == "Calculate the square root of a number"
        
        # Test execute with valid input
        result = SquareRootPlugin.execute("16")
        assert result == Decimal('4')
        
        # Test execute with no arguments
        with pytest.raises(ValueError):
            SquareRootPlugin.execute()
        
        # Test execute with negative number
        with pytest.raises(ValueError):
            SquareRootPlugin.execute("-4")
    
    def test_power_plugin(self):
        """Test the PowerPlugin."""
        # Test get_command and get_description
        assert PowerPlugin.get_command() == "power"
        assert PowerPlugin.get_description() == "Calculate a number raised to a power"
        
        # Test execute with valid input
        result = PowerPlugin.execute("2", "3")
        assert result == Decimal('8')
        
        # Test execute with no arguments
        with pytest.raises(ValueError):
            PowerPlugin.execute()
        
        # Test execute with only one argument
        with pytest.raises(ValueError):
            PowerPlugin.execute("2")
    
    def test_statistics_plugin(self):
        """Test the StatisticsPlugin."""
        # Test get_command and get_description
        assert StatisticsPlugin.get_command() == "stats"
        assert StatisticsPlugin.get_description() == "Calculate statistics (mean, min, max) on a list of numbers"
        
        # Test execute with valid input
        result = StatisticsPlugin.execute("10", "20", "30")
        assert result["count"] == 3
        assert result["mean"] == Decimal('20')
        assert result["min"] == Decimal('10')
        assert result["max"] == Decimal('30')
        
        # Test execute with no arguments
        with pytest.raises(ValueError):
            StatisticsPlugin.execute()
