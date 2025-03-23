"""
Tests for the main REPL interface.
"""
import io
import sys
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal

from main import CalculatorREPL, main

class TestCalculatorREPL:
    """Tests for the CalculatorREPL class."""
    
    @pytest.fixture
    def repl(self):
        """Fixture to provide a REPL instance for each test."""
        return CalculatorREPL()
    
    def test_init(self, repl):
        """Test that REPL initializes correctly."""
        assert repl.prompt == "calc> "
        assert repl.intro.startswith("Welcome")
        assert hasattr(repl, 'history_facade')
        assert hasattr(repl, 'plugin_manager')
    
    def test_parse_args(self, repl):
        """Test the _parse_args method."""
        args = repl._parse_args("10 20 30")
        assert args == ["10", "20", "30"]
        
        args = repl._parse_args("")
        assert args == []
    
    @patch('builtins.print')
    def test_do_add(self, mock_print, repl):
        """Test the do_add method."""
        # Test with valid arguments
        repl.do_add("10 5")
        mock_print.assert_called_with("Result: 15")
        
        # Test with invalid number of arguments
        repl.do_add("10")
        mock_print.assert_called_with("Error: add command requires exactly 2 numbers")
        
        # Test with invalid arguments
        repl.do_add("10 abc")
        assert "Error" in mock_print.call_args[0][0]
    
    @patch('builtins.print')
    def test_do_subtract(self, mock_print, repl):
        """Test the do_subtract method."""
        # Test with valid arguments
        repl.do_subtract("10 5")
        mock_print.assert_called_with("Result: 5")
        
        # Test with invalid number of arguments
        repl.do_subtract("10")
        mock_print.assert_called_with("Error: subtract command requires exactly 2 numbers")
    
    @patch('builtins.print')
    def test_do_multiply(self, mock_print, repl):
        """Test the do_multiply method."""
        # Test with valid arguments
        repl.do_multiply("10 5")
        mock_print.assert_called_with("Result: 50")
        
        # Test with invalid number of arguments
        repl.do_multiply("10")
        mock_print.assert_called_with("Error: multiply command requires exactly 2 numbers")
    
    @patch('builtins.print')
    def test_do_divide(self, mock_print, repl):
        """Test the do_divide method."""
        # Test with valid arguments
        repl.do_divide("10 5")
        mock_print.assert_called_with("Result: 2")
        
        # Test with invalid number of arguments
        repl.do_divide("10")
        mock_print.assert_called_with("Error: divide command requires exactly 2 numbers")
        
        # Test division by zero
        repl.do_divide("10 0")
        assert "Error" in mock_print.call_args[0][0]
    
    @patch('builtins.print')
    def test_do_history(self, mock_print, repl):
        """Test the do_history method."""
        # Add some calculations to history
        repl.do_add("10 5")
        
        # Test showing history
        repl.do_history("")
        assert mock_print.called
        
        # Test clearing history
        repl.do_history("clear")
        mock_print.assert_called_with("History cleared")
        
        # Test unknown history command
        repl.do_history("unknown")
        mock_print.assert_any_call("Unknown history command: unknown")
        mock_print.assert_any_call("Available commands: clear, save, load, delete, stats")
    
    @patch('builtins.print')
    def test_do_menu(self, mock_print, repl):
        """Test the do_menu method."""
        repl.do_menu("")
        assert mock_print.called
        
        # Just check that print was called multiple times
        assert mock_print.call_count > 1
    
    def test_do_exit(self, repl):
        """Test the do_exit method."""
        result = repl.do_exit("")
        assert result is True
    
    @patch('builtins.print')
    def test_default(self, mock_print, repl):
        """Test the default method."""
        # Test with unknown command
        repl.default("unknown")
        mock_print.assert_any_call("Unknown command: unknown")
        
        # Test with plugin command (assuming sqrt plugin is loaded)
        repl.plugin_manager.load_plugins()
        repl.default("sqrt 16")
        assert "Result: 4" in mock_print.call_args[0][0]
    
    def test_emptyline(self, repl):
        """Test the emptyline method."""
        # emptyline should do nothing
        assert repl.emptyline() is None

class TestMain:
    """Tests for the main function."""
    
    @patch('main.CalculatorREPL')
    def test_main_success(self, mock_repl):
        """Test that main runs successfully."""
        # Setup mock
        mock_instance = MagicMock()
        mock_repl.return_value = mock_instance
        
        # Call main
        result = main()
        
        # Check that REPL was created and cmdloop was called
        mock_repl.assert_called_once()
        mock_instance.cmdloop.assert_called_once()
        assert result == 0
    
    @patch('main.CalculatorREPL')
    @patch('builtins.print')
    def test_main_exception(self, mock_print, mock_repl):
        """Test that main handles exceptions."""
        # Setup mock to raise an exception
        mock_repl.side_effect = Exception("Test exception")
        
        # Call main
        result = main()
        
        # Check that exception was handled
        mock_print.assert_called_with("An error occurred: Test exception")
        assert result == 1
