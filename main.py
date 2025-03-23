"""
Main entry point for the calculator application.
Implements a Read-Eval-Print Loop (REPL) for interacting with the calculator.
"""
import os
import sys
import cmd
import re
from decimal import Decimal, InvalidOperation
from typing import List, Dict, Any, Optional

from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.calculation_history import get_history_facade
from calculator.plugins import get_plugin_manager
from calculator.logger import get_logger

# Get logger instance
logger = get_logger()

class CalculatorREPL(cmd.Cmd):
    """
    Command-line interface for the calculator application.
    Implements the Command pattern for handling user commands.
    """
    intro = "Welcome to the Better Calculator! Type 'help' for a list of commands."
    prompt = "calc> "
    
    def __init__(self):
        """Initialize the REPL with required components."""
        super().__init__()
        self.history_facade = get_history_facade()
        self.plugin_manager = get_plugin_manager()
        
        # Load plugins
        self.plugin_manager.load_plugins()
        logger.info("Calculator REPL initialized")
    
    def do_add(self, arg: str) -> None:
        """
        Add two numbers: add <a> <b>
        Example: add 5 3
        """
        args = self._parse_args(arg)
        if len(args) != 2:
            print("Error: add command requires exactly 2 numbers")
            return
        
        try:
            a, b = Decimal(args[0]), Decimal(args[1])
            calculation = Calculation(a, b, add)
            result = self.history_facade.add_calculation(calculation)
            print(f"Result: {result}")
        except (InvalidOperation, ValueError) as e:
            print(f"Error: {e}")
    
    def do_subtract(self, arg: str) -> None:
        """
        Subtract two numbers: subtract <a> <b>
        Example: subtract 10 4
        """
        args = self._parse_args(arg)
        if len(args) != 2:
            print("Error: subtract command requires exactly 2 numbers")
            return
        
        try:
            a, b = Decimal(args[0]), Decimal(args[1])
            calculation = Calculation(a, b, subtract)
            result = self.history_facade.add_calculation(calculation)
            print(f"Result: {result}")
        except (InvalidOperation, ValueError) as e:
            print(f"Error: {e}")
    
    def do_multiply(self, arg: str) -> None:
        """
        Multiply two numbers: multiply <a> <b>
        Example: multiply 6 7
        """
        args = self._parse_args(arg)
        if len(args) != 2:
            print("Error: multiply command requires exactly 2 numbers")
            return
        
        try:
            a, b = Decimal(args[0]), Decimal(args[1])
            calculation = Calculation(a, b, multiply)
            result = self.history_facade.add_calculation(calculation)
            print(f"Result: {result}")
        except (InvalidOperation, ValueError) as e:
            print(f"Error: {e}")
    
    def do_divide(self, arg: str) -> None:
        """
        Divide two numbers: divide <a> <b>
        Example: divide 20 5
        """
        args = self._parse_args(arg)
        if len(args) != 2:
            print("Error: divide command requires exactly 2 numbers")
            return
        
        try:
            a, b = Decimal(args[0]), Decimal(args[1])
            calculation = Calculation(a, b, divide)
            result = self.history_facade.add_calculation(calculation)
            print(f"Result: {result}")
        except (InvalidOperation, ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
    
    def do_history(self, arg: str) -> None:
        """
        Show calculation history.
        Optional arguments:
          clear - Clear the history
          save [filename] - Save history to a file (default: calculation_history.csv)
          load [filename] - Load history from a file (default: calculation_history.csv)
          delete [filename] - Delete history file (default: calculation_history.csv)
          stats - Show statistics about the history
        """
        args = self._parse_args(arg)
        command = args[0].lower() if args else ""
        
        try:
            if not command:
                # Show history
                history = self.history_facade.get_history()
                if history.empty:
                    print("No calculations in history")
                else:
                    print(history.to_string(index=False))
            
            elif command == "clear":
                # Clear history
                self.history_facade.clear_history()
                print("History cleared")
            
            elif command == "save":
                # Save history to file
                filename = args[1] if len(args) > 1 else None
                self.history_facade.save_history(filename)
                print(f"History saved to {filename or 'calculation_history.csv'}")
            
            elif command == "load":
                # Load history from file
                filename = args[1] if len(args) > 1 else None
                self.history_facade.load_history(filename)
                print(f"History loaded from {filename or 'calculation_history.csv'}")
            
            elif command == "delete":
                # Delete history file
                filename = args[1] if len(args) > 1 else None
                self.history_facade.delete_history_file(filename)
                print(f"History file {filename or 'calculation_history.csv'} deleted")
            
            elif command == "stats":
                # Show history statistics
                stats = self.history_facade.get_statistics()
                if stats["count"] == 0:
                    print("No calculations in history")
                else:
                    print(f"Total calculations: {stats['count']}")
                    print(f"Operations used: {stats['operations']}")
                    print(f"Average result: {stats['avg_result']}")
                    print(f"Minimum result: {stats['min_result']}")
                    print(f"Maximum result: {stats['max_result']}")
            
            else:
                print(f"Unknown history command: {command}")
                print("Available commands: clear, save, load, delete, stats")
        
        except Exception as e:
            print(f"Error: {e}")
    
    def do_menu(self, arg: str) -> None:
        """
        Show available commands menu.
        """
        print("\nBuilt-in Commands:")
        print("  add <a> <b> - Add two numbers")
        print("  subtract <a> <b> - Subtract two numbers")
        print("  multiply <a> <b> - Multiply two numbers")
        print("  divide <a> <b> - Divide two numbers")
        print("  history [subcommand] - Manage calculation history")
        print("  menu - Show this menu")
        print("  exit - Exit the calculator")
        
        # Show plugin commands
        plugin_descriptions = self.plugin_manager.get_plugin_descriptions()
        if plugin_descriptions:
            print("\nPlugin Commands:")
            for command, description in plugin_descriptions.items():
                print(f"  {command} - {description}")
        
        print()  # Empty line for readability
    
    def do_exit(self, arg: str) -> bool:
        """
        Exit the calculator.
        """
        print("Goodbye!")
        return True
    
    def default(self, line: str) -> None:
        """
        Handle unknown commands by checking if they are plugin commands.
        """
        # Parse the command and arguments
        match = re.match(r"(\w+)(.*)", line)
        if not match:
            print(f"Unknown command: {line}")
            return
        
        command = match.group(1)
        arg_str = match.group(2).strip()
        args = self._parse_args(arg_str)
        
        # Check if it's a plugin command
        try:
            if command in self.plugin_manager.get_plugin_commands():
                result = self.plugin_manager.execute_plugin(command, *args)
                print(f"Result: {result}")
            else:
                print(f"Unknown command: {command}")
                print("Type 'menu' to see available commands")
        except Exception as e:
            print(f"Error: {e}")
    
    def emptyline(self) -> None:
        """Do nothing on empty line."""
        pass
    
    def _parse_args(self, arg_str: str) -> List[str]:
        """
        Parse a string of arguments into a list.
        
        Args:
            arg_str: String containing space-separated arguments
            
        Returns:
            List of argument strings
        """
        return arg_str.split()


def main():
    """Main entry point for the calculator application."""
    try:
        # Configure logging from environment variables
        logger.info("Starting calculator application")
        
        # Start the REPL
        repl = CalculatorREPL()
        repl.cmdloop()
    
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
