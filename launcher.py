#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os

import modules.utils

# Define different message types with colored formatting
info_character = '<>'
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

# version = "1.0"
# launcher_dir = '/opt/ppm'
# cache_dir = '/var/cache/ppm'
# config_dir = '/etc/ppm'
# modules_dir = '/opt/ppm/modules'
# locale_dir = '/opt/ppm/localization'
version = "1.0"
launcher_dir = '.'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
modules_dir = './modules'
locale_dir = './localization'


init(autoreset=False) # init colorama
sys.setrecursionlimit(1500) 
sys.path.append(modules_dir) # Add custom path for ppm modules
import modules.dpkg
import modules.init
import modules.lock

print(f'ppm {version}')

def print_help():
    """
    Print help information about the usage of the ppm command.
    """
    print(f"""
Usage: ppm [options] command

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at [https://github.com/Stevesuk0/ppm/issues].

This software is free and follows the GNU General Public License v2.

Common commands:
init         Initialize configuration files and software sources""")



def main():
    if modules.utils.check_is_root() is False:
        # print("Please run ppm as root permissions.")
        
        
        path = os.getcwd()
        print(f"{warn} Running ppm as normal user.")
        return_code = os.system(f"pkexec bash -c 'cd {path}; {" ".join(sys.argv)}'") # run as root
        if return_code != 256:
            print(f"{error} Can't running ppm as root.")
        exit()
    

    # Check if there are enough arguments provided to the script
    if len(sys.argv) < 2:
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
