"""
Calculation History module for the calculator application.
Uses Pandas for efficient data handling and storage of calculation history.
Implements the Facade pattern to provide a simplified interface for complex Pandas operations.
"""
import os
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Callable

import pandas as pd

from calculator.calculation import Calculation
from calculator.logger import get_logger

logger = get_logger()

class CalculationHistoryFacade:
    """
    Facade pattern implementation for calculation history management.
    Provides a simplified interface for complex Pandas data manipulations.
    """
    _instance = None
    _dataframe = None
    _default_csv_path = "calculation_history.csv"

    def __new__(cls):
        """Implement Singleton pattern for history management."""
        if cls._instance is None:
            cls._instance = super(CalculationHistoryFacade, cls).__new__(cls)
            cls._instance._initialize_dataframe()
        return cls._instance

    def _initialize_dataframe(self):
        """Initialize an empty DataFrame with the required columns."""
        self._dataframe = pd.DataFrame(columns=[
            'timestamp', 'operation', 'a', 'b', 'result'
        ])
        logger.info("Initialized empty calculation history DataFrame")

    def add_calculation(self, calculation: Calculation):
        """
        Add a calculation to the history.
        
        Args:
            calculation: The Calculation object to add to history
        """
        try:
            # Perform the calculation to get the result
            result = calculation.perform()
            
            # Create a new row for the DataFrame
            new_row = pd.DataFrame([{
                'timestamp': datetime.now(),
                'operation': calculation.operation.__name__,
                'a': float(calculation.a),  # Convert Decimal to float for pandas
                'b': float(calculation.b),  # Convert Decimal to float for pandas
                'result': float(result)     # Convert Decimal to float for pandas
            }])
            
            # Append the new row to the DataFrame
            self._dataframe = pd.concat([self._dataframe, new_row], ignore_index=True)
            
            logger.info(f"Added calculation to history: {calculation}")
            return result
        except Exception as e:
            logger.error(f"Error adding calculation to history: {e}")
            raise

    def get_history(self) -> pd.DataFrame:
        """
        Get the entire calculation history as a DataFrame.
        
        Returns:
            DataFrame containing all calculations
        """
        logger.debug("Retrieved calculation history")
        return self._dataframe.copy()

    def get_history_as_dict(self) -> List[Dict[str, Any]]:
        """
        Get the calculation history as a list of dictionaries.
        
        Returns:
            List of dictionaries representing calculations
        """
        logger.debug("Retrieved calculation history as dict")
        return self._dataframe.to_dict('records')

    def clear_history(self):
        """Clear the calculation history."""
        self._initialize_dataframe()
        logger.info("Cleared calculation history")

    def save_history(self, filepath: Optional[str] = None):
        """
        Save the calculation history to a CSV file.
        
        Args:
            filepath: Path to save the CSV file, defaults to _default_csv_path
        """
        filepath = filepath or self._default_csv_path
        try:
            self._dataframe.to_csv(filepath, index=False)
            logger.info(f"Saved calculation history to {filepath}")
        except Exception as e:
            logger.error(f"Error saving calculation history: {e}")
            raise

    def load_history(self, filepath: Optional[str] = None):
        """
        Load calculation history from a CSV file.
        
        Args:
            filepath: Path to load the CSV file from, defaults to _default_csv_path
        """
        filepath = filepath or self._default_csv_path
        try:
            if os.path.exists(filepath):
                self._dataframe = pd.read_csv(filepath)
                logger.info(f"Loaded calculation history from {filepath}")
            else:
                logger.warning(f"History file {filepath} not found")
        except Exception as e:
            logger.error(f"Error loading calculation history: {e}")
            raise

    def delete_history_file(self, filepath: Optional[str] = None):
        """
        Delete the calculation history file.
        
        Args:
            filepath: Path to the history file to delete, defaults to _default_csv_path
        """
        filepath = filepath or self._default_csv_path
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted calculation history file {filepath}")
            else:
                logger.warning(f"History file {filepath} not found")
        except Exception as e:
            logger.error(f"Error deleting calculation history file: {e}")
            raise

    def filter_by_operation(self, operation_name: str) -> pd.DataFrame:
        """
        Filter history by operation name.
        
        Args:
            operation_name: Name of the operation to filter by
            
        Returns:
            DataFrame containing filtered calculations
        """
        filtered = self._dataframe[self._dataframe['operation'] == operation_name]
        logger.debug(f"Filtered history by operation: {operation_name}")
        return filtered.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the calculation history.
        
        Returns:
            Dictionary containing statistics
        """
        if self._dataframe.empty:
            logger.debug("No calculations in history for statistics")
            return {"count": 0}
        
        stats = {
            "count": len(self._dataframe),
            "operations": self._dataframe['operation'].value_counts().to_dict(),
            "avg_result": self._dataframe['result'].mean(),
            "min_result": self._dataframe['result'].min(),
            "max_result": self._dataframe['result'].max()
        }
        logger.debug("Generated calculation history statistics")
        return stats

# Global instance for easy access
def get_history_facade() -> CalculationHistoryFacade:
    """
    Get the calculation history facade instance.
    
    Returns:
        Singleton instance of CalculationHistoryFacade
    """
    return CalculationHistoryFacade()
