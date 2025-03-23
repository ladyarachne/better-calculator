"""
Logger module for the calculator application.
Implements a comprehensive logging system with configurable levels and outputs.
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

class LoggerSingleton:
    """
    Singleton class for managing application logging.
    Provides a centralized logging configuration that can be accessed throughout the application.
    """
    _instance = None
    _logger = None

    def __new__(cls):
        """Ensure only one instance of the logger exists."""
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        """Configure the logger based on environment variables."""
        # Get logging level from environment variable, default to INFO
        log_level_name = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO').upper()
        log_level = getattr(logging, log_level_name, logging.INFO)
        
        # Get log file path from environment variable, default to None (console only)
        log_file = os.environ.get('CALCULATOR_LOG_FILE')
        
        # Create logger
        self._logger = logging.getLogger('calculator')
        self._logger.setLevel(log_level)
        self._logger.handlers = []  # Clear any existing handlers
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # Create file handler if log file is specified
        if log_file:
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self._logger

# Global function to get the logger instance
def get_logger() -> logging.Logger:
    """
    Get the application logger.
    Returns a configured logger that can be used throughout the application.
    """
    return LoggerSingleton().get_logger()
