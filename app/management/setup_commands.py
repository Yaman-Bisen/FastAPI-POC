import typer
import pkgutil
import importlib
from typing import Dict, Type


cli = typer.Typer(name="app")

# Base Command class
class Command:
    name = "command"
    help = "Base command class"
    
    def handle(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement handle()")

command_registry: Dict[str, Type[Command]] = {}

def register_command(command_class):
    command_name = command_class.name
    
    @cli.command(name=command_name, help=command_class.help)
    def command_wrapper(**kwargs):
        cmd = command_class()
        cmd.handle(**kwargs)
    
    command_registry[command_name] = command_class
    return command_class

def setup_commands():
    try:
        import app.management.commands
        
        package_path = app.management.commands.__path__
        for _, name, is_pkg in pkgutil.iter_modules(package_path):
            if not is_pkg:
                importlib.import_module(f'app.management.commands.{name}')
        
        print(f"Registered {len(command_registry)} management commands")
    except ImportError as e:
        import traceback
        traceback.print_exc()
        print(f"Error importing commands: {e}")
    
    return command_registry