"""
Sample plugin for the calculator application.
Demonstrates how to create a plugin that can be loaded by the plugin system.
"""
from decimal import Decimal
from typing import List, Any

from calculator.plugins import PluginInterface
from calculator.logger import get_logger

logger = get_logger()

class SquareRootPlugin(PluginInterface):
    """
    Plugin that calculates the square root of a number.
    """
    @classmethod
    def get_command(cls) -> str:
        """Get the command name for this plugin."""
        return "sqrt"
    
    @classmethod
    def get_description(cls) -> str:
        """Get the description for this plugin."""
        return "Calculate the square root of a number"
    
    @classmethod
    def execute(cls, *args) -> Any:
        """
        Execute the square root calculation.
        
        Args:
            args[0]: The number to calculate the square root of
            
        Returns:
            The square root of the number
            
        Raises:
            ValueError: If no number is provided or the number is negative
        """
        if not args or len(args) < 1:
            raise ValueError("Please provide a number to calculate the square root of")
        
        try:
            number = Decimal(args[0])
            if number < 0:
                raise ValueError("Cannot calculate square root of a negative number")
            
            result = number.sqrt()
            logger.info(f"Calculated square root of {number}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error calculating square root: {e}")
            raise


class PowerPlugin(PluginInterface):
    """
    Plugin that calculates a number raised to a power.
    """
    @classmethod
    def get_command(cls) -> str:
        """Get the command name for this plugin."""
        return "power"
    
    @classmethod
    def get_description(cls) -> str:
        """Get the description for this plugin."""
        return "Calculate a number raised to a power"
    
    @classmethod
    def execute(cls, *args) -> Any:
        """
        Execute the power calculation.
        
        Args:
            args[0]: The base number
            args[1]: The exponent
            
        Returns:
            The base raised to the exponent
            
        Raises:
            ValueError: If not enough arguments are provided
        """
        if not args or len(args) < 2:
            raise ValueError("Please provide a base and exponent (e.g., power 2 3)")
        
        try:
            base = Decimal(args[0])
            exponent = Decimal(args[1])
            
            result = base ** exponent
            logger.info(f"Calculated {base} raised to {exponent}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error calculating power: {e}")
            raise


class StatisticsPlugin(PluginInterface):
    """
    Plugin that calculates basic statistics on a list of numbers.
    """
    @classmethod
    def get_command(cls) -> str:
        """Get the command name for this plugin."""
        return "stats"
    
    @classmethod
    def get_description(cls) -> str:
        """Get the description for this plugin."""
        return "Calculate statistics (mean, min, max) on a list of numbers"
    
    @classmethod
    def execute(cls, *args) -> Any:
        """
        Calculate statistics on a list of numbers.
        
        Args:
            *args: List of numbers to calculate statistics for
            
        Returns:
            Dictionary containing statistics
            
        Raises:
            ValueError: If no numbers are provided
        """
        if not args:
            raise ValueError("Please provide numbers to calculate statistics for")
        
        try:
            numbers = [Decimal(arg) for arg in args]
            
            # Calculate statistics
            mean = sum(numbers) / len(numbers)
            minimum = min(numbers)
            maximum = max(numbers)
            
            result = {
                "mean": mean,
                "min": minimum,
                "max": maximum,
                "count": len(numbers)
            }
            
            logger.info(f"Calculated statistics for {len(numbers)} numbers")
            return result
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            raise
