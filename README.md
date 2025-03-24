# Better Calculator

A Python-based calculator application with advanced features including a REPL interface, plugin system, calculation history management, and professional logging. 
## Project Demonstration
[Click here to watch the demo video](https://drive.google.com/file/d/1BiJx9PHATZhtLNK5KYTnUdthpk15xnB-/view?usp=sharing)


## Features

### 1. Command-Line Interface (REPL)

The calculator provides a Read-Eval-Print Loop (REPL) interface for direct interaction, supporting:
- Basic arithmetic operations (add, subtract, multiply, divide)
- Calculation history management
- Plugin system for extended functionality

### 2. Plugin System

The application includes a flexible plugin system that allows seamless integration of new commands or features without modifying the core code:
- Dynamically loads and integrates plugins
- Provides a "menu" command to list all available plugin commands
- Easy to extend with custom plugins

### 3. Calculation History Management

Uses Pandas for efficient calculation history management:
- View, save, load, and clear calculation history
- Export history to CSV files
- Generate statistics about calculation history

### 4. Professional Logging

Comprehensive logging system that records:
- Application operations
- Data manipulations
- Errors and informational messages
- Configurable logging levels via environment variables

### 5. Design Patterns

The application implements several design patterns for a scalable architecture:
- **Facade Pattern**: Simplifies complex Pandas data manipulations
- **Command Pattern**: Structures commands within the REPL
- **Factory Method Pattern**: Creates plugin instances dynamically
- **Singleton Pattern**: Ensures single instances of key components
- **Strategy Pattern**: Enables flexible calculation operations

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/better-calculator.git
   cd better-calculator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables (optional):
   - Create a `.env` file with the following variables:
     ```
     CALCULATOR_LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
     CALCULATOR_LOG_FILE=calculator.log  # Path to log file (optional)
     ```

## Usage

### Starting the Calculator

Run the calculator with:
```
python main.py
```

### Basic Commands

- `add <a> <b>` - Add two numbers
- `subtract <a> <b>` - Subtract two numbers
- `multiply <a> <b>` - Multiply two numbers
- `divide <a> <b>` - Divide two numbers
- `history` - Show calculation history
- `menu` - Show available commands
- `exit` - Exit the calculator

### History Management

- `history` - Show calculation history
- `history clear` - Clear the history
- `history save [filename]` - Save history to a file
- `history load [filename]` - Load history from a file
- `history delete [filename]` - Delete history file
- `history stats` - Show statistics about the history

### Plugin Commands

The calculator comes with several built-in plugins:
- `sqrt <number>` - Calculate the square root of a number
- `power <base> <exponent>` - Calculate a number raised to a power
- `stats <num1> <num2> ...` - Calculate statistics on a list of numbers

## Architecture

### Core Components

1. **Calculator**: Provides basic arithmetic operations
2. **Calculation**: Encapsulates a single calculation with two operands and an operation
3. **CalculationHistoryFacade**: Manages calculation history using Pandas
4. **PluginManager**: Handles loading and executing plugins
5. **LoggerSingleton**: Provides centralized logging configuration

### Design Patterns

#### Facade Pattern

The `CalculationHistoryFacade` class provides a simplified interface for complex Pandas data manipulations, hiding the details of DataFrame operations from the rest of the application.

#### Command Pattern

The REPL interface implements the Command pattern through the `cmd.Cmd` class, with each command encapsulated in a separate method (`do_add`, `do_subtract`, etc.).

#### Factory Method Pattern

The `PluginManager` implements the Factory Method pattern to create plugin instances dynamically based on the command entered by the user.

#### Singleton Pattern

Several components use the Singleton pattern to ensure only one instance exists:
- `LoggerSingleton`: Ensures a single logger configuration
- `CalculationHistoryFacade`: Maintains a single history instance
- `PluginManager`: Provides a single plugin management system

#### Strategy Pattern

The `Calculation` class uses the Strategy pattern by accepting an operation function as a parameter, allowing for flexible calculation strategies.

## Extending with Plugins

To create a new plugin:

1. Create a new Python file in the `calculator/plugins` directory
2. Define a class that inherits from `PluginInterface`
3. Implement the required methods:
   - `get_command()`: Returns the command name
   - `get_description()`: Returns a description of the plugin
   - `execute(*args)`: Implements the plugin functionality

Example:
```python
from calculator.plugins import PluginInterface
from decimal import Decimal

class MyPlugin(PluginInterface):
    @classmethod
    def get_command(cls):
        return "mycommand"
    
    @classmethod
    def get_description(cls):
        return "Description of my command"
    
    @classmethod
    def execute(cls, *args):
        # Implement your functionality here
        return result
```

## Testing

Run tests with:
```
pytest
```

For test coverage report:
```
pytest --cov=calculator
```

## Implementation Details

### Design Patterns Implementation

1. **Facade Pattern**: 
   - [CalculationHistoryFacade](calculator/calculation_history.py) - Lines 20-175
   - This pattern provides a simplified interface for complex Pandas operations, hiding the implementation details from the rest of the application.
   - Example: The `add_calculation` method handles all the complexity of converting Decimal objects to float, creating a DataFrame row, and appending it to the history.

2. **Command Pattern**:
   - [CalculatorREPL](main.py) - Lines 19-196
   - Each command in the REPL is encapsulated in a separate method (do_add, do_subtract, etc.), following the Command pattern.
   - Example: The `do_add` method encapsulates the logic for adding two numbers and storing the result in history.

3. **Factory Method Pattern**:
   - [PluginManager](calculator/plugins/__init__.py) - Lines 47-107
   - The `load_plugins` method dynamically discovers and loads plugins, creating instances as needed.
   - Example: The `execute_plugin` method creates and executes plugin instances based on the command name.

4. **Singleton Pattern**:
   - [LoggerSingleton](calculator/logger.py) - Lines 13-45
   - [CalculationHistoryFacade](calculator/calculation_history.py) - Lines 20-35
   - [PluginManager](calculator/plugins/__init__.py) - Lines 47-59
   - These classes ensure only one instance exists throughout the application.
   - Example: The `__new__` method in LoggerSingleton checks if an instance already exists and returns it if it does.

5. **Strategy Pattern**:
   - [Calculation](calculator/calculation.py) - Lines 19-45
   - The Calculation class accepts an operation function as a parameter, allowing for flexible calculation strategies.
   - Example: The `perform` method calls the operation function with the operands, regardless of what specific operation it is.

### Environment Variables Usage

The application uses environment variables for configuration, particularly for the logging system:

- [Logger Configuration](calculator/logger.py) - Lines 28-33
- The logger reads environment variables to configure the logging level and output file:
  - `CALCULATOR_LOG_LEVEL`: Sets the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `CALCULATOR_LOG_FILE`: Sets the path to the log file (if not set, logs only to console)
- Example usage in code:
  ```python
  log_level_name = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO').upper()
  log_level = getattr(logging, log_level_name, logging.INFO)
  log_file = os.environ.get('CALCULATOR_LOG_FILE')
  ```

### Logging Implementation

The application implements a comprehensive logging system:

- [LoggerSingleton](calculator/logger.py) - Lines 13-45
- Logs are used throughout the application to record:
  - Information messages: [Example in PluginManager](calculator/plugins/__init__.py) - Line 101
  - Error messages: [Example in CalculationHistoryFacade](calculator/calculation_history.py) - Line 67
  - Debug messages: [Example in CalculationHistoryFacade](calculator/calculation_history.py) - Line 93
- The logging system supports both console and file output, with configurable levels.

### Exception Handling

The application uses both LBYL (Look Before You Leap) and EAFP (Easier to Ask for Forgiveness than Permission) approaches:

1. **LBYL Examples**:
   - [PluginManager](calculator/plugins/__init__.py) - Lines 169-171
   - Checking if a plugin exists before attempting to execute it:
     ```python
     plugin_class = self.get_plugin(command)
     if plugin_class is None:
         raise ValueError(f"Plugin '{command}' not found")
     ```

2. **EAFP Examples**:
   - [CalculationHistoryFacade](calculator/calculation_history.py) - Lines 56-68
   - Using try/except to handle potential errors during calculation:
     ```python
     try:
         # Perform the calculation to get the result
         result = calculation.perform()
         # ... more code ...
         return result
     except Exception as e:
         logger.error(f"Error adding calculation to history: {e}")
         raise
     ```
   - [SquareRootPlugin](calculator/plugins/sample_plugin.py) - Lines 36-47
   - Using try/except to handle potential errors during square root calculation:
     ```python
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
     ```

### GitHub Actions Configuration

The project uses GitHub Actions for continuous integration:

- [pytest.yml](.github/workflows/pytest.yml)
- The workflow runs on push and pull requests to the main branch
- It sets up Python, installs dependencies, and runs tests with coverage
- The workflow ensures that all tests pass and maintains code quality

## License

[MIT License](LICENSE)
