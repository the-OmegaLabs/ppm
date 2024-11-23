import os
import sys
import requests
import json
from colorama import Fore, Style, init

# Color constants for output
info = f"{Fore.CYAN}[INFO]{Style.RESET_ALL}"
success = f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL}"
error = f"{Fore.RED}[ERROR]{Style.RESET_ALL}"

class manager:
    def __init__(self):
        self.cache_dir = r'C:\ProgramData\ppm\cache'
        self.all_packages = self.load_all_packages()
        self.is_windows = sys.platform.startswith('win32')

    def load_all_packages(self):
        if os.path.exists(self.cache_dir):
            return os.listdir(self.cache_dir)
        return []

    def update_packages(self):
        """Update package metadata from the repository."""
        if self.is_windows:
            print(f"{info} Using winget-compatible sources...")
            os.makedirs(self.cache_dir, exist_ok=True)
            url = "https://winget.azureedge.net/cache/manifests.zip"
            local_file = os.path.join(self.cache_dir, "manifests.zip")
            try:
                print(f"{info} Downloading winget manifests...")
                response = requests.get(url)
                with open(local_file, "wb") as f:
                    f.write(response.content)
                print(f"{success} Winget manifests downloaded successfully.")
                # Unzip and process if needed
            except Exception as e:
                print(f"{error} Failed to download manifests: {e}")
        else:
            print(f"{info} Linux/other OS package update not implemented.")

    def install_package(self, dolist):
        if self.is_windows:
            for package_name in dolist:
                print(f"{info} Installing {package_name} using winget...")
                os.system(f"winget install --silent --exact {package_name}")
        else:
            print(f"{error} Install command is only implemented for Windows.")

    def search_package(self, target):
        if self.is_windows:
            print(f"{info} Searching for {target} in winget repositories...")
            os.system(f"winget search {target}")
        else:
            print(f"{error} Search command is only implemented for Windows.")

class modules:
    def root_check(self):
        if sys.platform.startswith('win32'):
            return True
        else:
            print(f"{info} Root check is irrelevant for non-Windows platforms.")
            return True

    def init(self):
        if not self.check_winget_installed():
            return
        if sys.platform.startswith('win32'):
            os.makedirs(r'C:\ProgramData\ppm', exist_ok=True)
            with open(r'C:\ProgramData\ppm\repo.json', 'w') as f:
                json.dump(
                    [{"name": "Winget", "type": "winget", "url": "https://winget.azureedge.net"}],
                    f,
                    indent=4,
                )
            print(f"{success} Successfully initialized configuration for Windows.")
        else:
            print(f"{error} Initialization only supported for Windows.")

    def check_winget_installed(self):
        if sys.platform.startswith('win32'):
            result = os.system("winget --version >nul 2>&1")
            if result == 0:
                print(f"{success} Winget is installed.")
                return True
            else:
                print(f"{error} Winget is not installed. Please install Winget to use this program.")
                return False
        else:
            print(f"{info} Winget check is irrelevant for non-Windows platforms.")
            return False

    def show_help(self):
        help_text = f"""
{info} Usage: ppm [command] [options]

Commands:
  install <package_name>  Install a package using winget.
  search <package_name>   Search for a package in winget repositories.
  update                  Update package metadata from the repository.
  init                    Initialize the configuration for Windows.
  help                    Show this help message.

Examples:
  ppm install Notepad++
  ppm search Firefox
  ppm update
  ppm init
  ppm help
"""
        print(help_text)

def main():
    if sys.platform.startswith('win32'):
        init(autoreset=True)  # Enable colorama for Windows
    else:
        init(autoreset=False)
        print(f"{error} This script is currently optimized for Windows.")

    modules_obj = modules()


    manager_obj = manager()

    if len(sys.argv) < 1:
        print(f"{error} Missing command. Use 'ppm help' for usage.")
        return

    command = sys.argv[1]
    if command == 'install' and len(sys.argv) == 3:
        manager_obj.install_package([sys.argv[2]])
    elif command == 'search' and len(sys.argv) == 3:
        manager_obj.search_package(sys.argv[2])
    elif command == 'update':
        manager_obj.update_packages()
    elif command == 'init':
        modules_obj.init()
    elif command == 'help':
        modules_obj.show_help()
    else:
        print(f"{error} Unknown command or invalid arguments.")

if __name__ == "__main__":
    main()
