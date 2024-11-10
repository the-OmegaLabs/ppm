#!/usr/bin/python3

import sys
sys.path.append('/opt/ppm') # Add custom path to system path to fix ModuleNotFoundError

from colorama import init, Fore, Style, Back
import os
import modules.dpkg
import modules.init
import modules.lock
from sys import argv, exit

init() # Initialize colorama for colored console text

version = "1.0"
info_character = '<>'

# Define different message types with colored formatting
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

print(f'ppm {version}')

def print_help():
    """
    Print help information about the usage of the ppm command.
    """
    print(f"""ppm {version}: Missing command
Usage: ppm [options] command

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at [https://github.com/Stevesuk0/ppm/issues].

This software is free and follows the GNU General Public License v2.

Common commands:
update       Update the package list
search       Search for packages by keyword
download     Download a package and its dependencies
install      Install a package and its dependencies
init         Initialize configuration files and software sources
reset        Force remove ppm process lock
syncdpkg     Synchronize the status of installed packages from dpkg""")

def main():
    print(f"{info} Starting main function...")
    
    # Check if the configuration directory exists
    if not os.path.exists('/etc/ppm'):
        print(f"{warn} Configuration directory not found. Initializing...")
        if modules.init.init_config():
            print(f"{success} Configuration initialized successfully.")
        else:
            print(f"{error} Failed to initialize configuration.")
            exit(1) # Exit if initialization fails

    # Check if there are enough arguments provided to the script
    if len(argv) < 2:
        print(f"{error} Not enough arguments provided.")
        print_help()
        exit(1) # Exit if no command is provided
    else:
        print(f"{success} Command line arguments are sufficient.")

if __name__ == "__main__":
    main()
else:
    print(f"{error} Directly importing ppm is not allowed for managing system packages.")
    print(f"{info} Ideally, you should be importing the modules of ppm, not the launcher.")
