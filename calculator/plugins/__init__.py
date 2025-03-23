"""
Plugin system for the calculator application.
Provides a flexible way to extend the calculator with new commands and features.
"""
import importlib
import inspect
import os
import pkgutil
from typing import Dict, List, Callable, Any, Optional

from calculator.logger import get_logger

logger = get_logger()

class PluginInterface:
    """
    Interface that all calculator plugins must implement.
    """
    @classmethod
    def get_command(cls) -> str:
        """
        Get the command name that will trigger this plugin.
        
        Returns:
            String representing the command name
        """
        raise NotImplementedError("Plugins must implement get_command")
    
    @classmethod
    def get_description(cls) -> str:
        """
        Get a description of what this plugin does.
        
        Returns:
            String describing the plugin functionality
        """
        raise NotImplementedError("Plugins must implement get_description")
    
    @classmethod
    def execute(cls, *args) -> Any:
        """
        Execute the plugin functionality.
        
        Args:
            *args: Variable length argument list passed from the REPL
            
        Returns:
            Result of the plugin execution
        """
        raise NotImplementedError("Plugins must implement execute")


class PluginManager:
    """
    Manager for loading and accessing calculator plugins.
    Implements the Factory Method pattern for creating plugin instances.
    """
    _instance = None
    _plugins: Dict[str, type] = {}
    
    def __new__(cls):
        """Implement Singleton pattern for plugin management."""
        if cls._instance is None:
            cls._instance = super(PluginManager, cls).__new__(cls)
            cls._instance._plugins = {}
        return cls._instance
    
    def load_plugins(self, plugin_package: str = "calculator.plugins"):
        """
        Dynamically load all plugins from the specified package.
        
        Args:
            plugin_package: Dot-separated path to the plugin package
        """
        self._plugins = {}
        
        # Import the package
        package = importlib.import_module(plugin_package)
        package_path = os.path.dirname(package.__file__)
        
        # Find all modules in the package
        for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
            if not is_pkg and module_name != "__init__":
                # Import the module
                module = importlib.import_module(f"{plugin_package}.{module_name}")
                
                # Find all classes in the module that are plugins
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, PluginInterface) and 
                        obj is not PluginInterface and
                        hasattr(obj, 'get_command') and
                        hasattr(obj, 'get_description') and
                        hasattr(obj, 'execute')):
                        
                        # Register the plugin
                        command = obj.get_command()
                        if command in self._plugins:
                            logger.warning(f"Plugin command '{command}' already registered. Overwriting.")
                        
                        self._plugins[command] = obj
                        logger.info(f"Loaded plugin: {command} - {obj.get_description()}")
    
    def get_plugin(self, command: str) -> Optional[type]:
        """
        Get a plugin by its command name.
        
        Args:
            command: The command name to look up
            
        Returns:
            The plugin class or None if not found
        """
        return self._plugins.get(command)
    
    def get_all_plugins(self) -> Dict[str, type]:
        """
        Get all registered plugins.
        
        Returns:
            Dictionary mapping command names to plugin classes
        """
        return self._plugins.copy()
    
    def get_plugin_commands(self) -> List[str]:
        """
        Get a list of all available plugin commands.
        
        Returns:
            List of command names
        """
        return list(self._plugins.keys())
    
    def get_plugin_descriptions(self) -> Dict[str, str]:
        """
        Get descriptions for all plugins.
        
        Returns:
            Dictionary mapping command names to descriptions
        """
        return {cmd: plugin.get_description() for cmd, plugin in self._plugins.items()}
    
    def execute_plugin(self, command: str, *args) -> Any:
        """
        Execute a plugin by its command name.
        
        Args:
            command: The command name to execute
            *args: Arguments to pass to the plugin
            
        Returns:
            Result of the plugin execution
            
        Raises:
            ValueError: If the plugin is not found
        """
        plugin_class = self.get_plugin(command)
        if plugin_class is None:
            raise ValueError(f"Plugin '{command}' not found")
        
        logger.info(f"Executing plugin: {command}")
        return plugin_class.execute(*args)

# Global instance for easy access
def get_plugin_manager() -> PluginManager:
    """
    Get the plugin manager instance.
    
    Returns:
        Singleton instance of PluginManager
    """
    return PluginManager()
