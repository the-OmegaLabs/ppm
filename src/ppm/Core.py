import atexit
import os
import importlib
import tempfile

class Manager:
    """
    ### `class`: Manager

    Main entry-point for the Plusto Package Manager.

    Plusto is a hybrid package manager designed for Omega Linux.
    Homepage: https://github.com/the-OmegaLabs/ppm
    """

    def __init__(self):
        self.version = 'dev-20251205'
        self.root_path = './data'
        self.commands = {}
        
        self._LOCK_FH = None

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

    def execute(self, command: str, arg=None):
        """
        Execute a registered command with an optional argument.

        Args:
            command (str): Name of the command to run (must be a key in self.commands).
            arg (Any, optional): Argument passed directly to the command's on_execute method.

        Raises:
            AttributeError: If the requested command is not found.

        Returns:
            None: The command's return value (if any) is ignored.
        """
        try:
            cmd = self.commands[command]
        except KeyError:
            raise AttributeError(f'Unknown command "{command}"') from None
        cmd.on_execute(arg)

    def hold_lock(self):
        """
        Acquire the global instance lock.

        Creates an empty lock file at `<root_path>/ppm.lock` if none exists;
        otherwise reports that another instance is already running.
        The lock is automatically removed when the process exits.

        Returns
        -------
        bool
            True  - lock acquired successfully  
            False - lock is held by another instance
        """
            
        lock_path = os.path.join(self.root_path, 'ppm.lock')
        
        if os.path.exists(lock_path):
            return False
        
        with open(lock_path, 'w') as f:
            f.write('')
            
            atexit.register(lambda: os.remove(lock_path))
        
        self._lock = True
        return True

    def init(self) -> bool:
        """
        Initialize manager by creating necessary directories.
        
        Returns:
            bool: True if initialization succeeded, False otherwise. Hold a lock can resolve the problem.
        """
        
        if not self._lock: return False

        os.makedirs(f'{self.root_path}/cache', exist_ok=True)
        os.makedirs(f'{self.root_path}/config', exist_ok=True)
        os.makedirs(f'{self.root_path}/locale', exist_ok=True)

        self._register_commands()

        return True