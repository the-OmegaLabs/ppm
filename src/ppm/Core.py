import os
import importlib

class Manager:
    """
    ### `class`: Manager

    The main initiator class of Plusto Package Manager.

    Plusto Package Manager is a hybrid software package manager for Omega Linux.
    More infomation: https://github.com/the-OmegaLabs/ppm
    """

    def __init__(self):
        self.version = 'dev-20251005'
        
        self.root_path = './data'

        self.commands = {}

    def _register_commands(self):
        module = importlib.import_module('ppm.Command')
        package_path = os.path.dirname(module.__file__)
        
        for filename in os.listdir(package_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3] 
                sub_module = importlib.import_module(f"ppm.Command.{module_name}")
                
                cmd_class = getattr(sub_module, "Command", None)
                if cmd_class:
                    self.commands[module_name] = cmd_class()

    def init(self) -> bool:
        """
        Initialize manager by creating necessary directories.
        
        Returns:
            bool: True if initialization succeeded, False otherwise.
        """

        os.makedirs(f'{self.root_path}/cache', exist_ok=True)
        os.makedirs(f'{self.root_path}/config', exist_ok=True)
        os.makedirs(f'{self.root_path}/locale', exist_ok=True)

        self._register_commands()

        return True