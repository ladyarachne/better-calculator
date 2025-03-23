"""
Tests for the logger module.
"""
import os
import logging
import pytest
from unittest.mock import patch, MagicMock

from calculator.logger import LoggerSingleton, get_logger

class TestLoggerSingleton:
    """Tests for the LoggerSingleton class."""
    
    def test_singleton_pattern(self):
        """Test that LoggerSingleton follows the Singleton pattern."""
        logger1 = LoggerSingleton()
        logger2 = LoggerSingleton()
        assert logger1 is logger2
    
    def test_get_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == 'calculator'
    
    @patch.dict(os.environ, {"CALCULATOR_LOG_LEVEL": "DEBUG"})
    def test_log_level_from_env(self):
        """Test that log level is set from environment variable."""
        # Reset the singleton instance to pick up the new environment variable
        LoggerSingleton._instance = None
        
        logger = LoggerSingleton().get_logger()
        assert logger.level == logging.DEBUG
    
    @patch.dict(os.environ, {"CALCULATOR_LOG_LEVEL": "INVALID"})
    def test_invalid_log_level_defaults_to_info(self):
        """Test that invalid log level defaults to INFO."""
        # Reset the singleton instance to pick up the new environment variable
        LoggerSingleton._instance = None
        
        logger = LoggerSingleton().get_logger()
        assert logger.level == logging.INFO
    
    @patch.dict(os.environ, {"CALCULATOR_LOG_FILE": "test.log"})
    def test_log_file_from_env(self):
        """Test that log file is set from environment variable."""
        # Reset the singleton instance to pick up the new environment variable
        LoggerSingleton._instance = None
        
        logger = LoggerSingleton().get_logger()
        
        # Check that there are at least 2 handlers (console and file)
        assert len(logger.handlers) >= 2
        
        # Check that one of the handlers is a FileHandler
        file_handlers = [h for h in logger.handlers if hasattr(h, 'baseFilename')]
        assert len(file_handlers) > 0
        
        # Clean up the test log file if it was created
        for handler in file_handlers:
            if os.path.exists(handler.baseFilename):
                handler.close()
                os.remove(handler.baseFilename)
    
    def test_logger_handlers(self):
        """Test that logger has the correct handlers."""
        # Reset the singleton instance
        LoggerSingleton._instance = None
        
        logger = LoggerSingleton().get_logger()
        
        # Check that there is at least one handler (console)
        assert len(logger.handlers) >= 1
        
        # Check that one of the handlers is a StreamHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) > 0

class TestLoggerFunctionality:
    """Tests for the logger functionality."""
    
    @pytest.fixture
    def logger(self):
        """Fixture to provide a logger for each test."""
        return get_logger()
    
    def test_logger_info(self, logger, caplog):
        """Test that logger.info works correctly."""
        with caplog.at_level(logging.INFO):
            logger.info("Test info message")
            assert "Test info message" in caplog.text
    
    def test_logger_error(self, logger, caplog):
        """Test that logger.error works correctly."""
        with caplog.at_level(logging.ERROR):
            logger.error("Test error message")
            assert "Test error message" in caplog.text
    
    def test_logger_debug(self, logger, caplog):
        """Test that logger.debug works correctly."""
        # Set the logger level to DEBUG for this test
        original_level = logger.level
        logger.setLevel(logging.DEBUG)
        
        with caplog.at_level(logging.DEBUG):
            logger.debug("Test debug message")
            assert "Test debug message" in caplog.text
        
        # Restore the original level
        logger.setLevel(original_level)
