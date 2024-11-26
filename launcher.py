#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os

# Define different message types with colored formatting
info_character = '##'
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

version = "0.1"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = '/opt/ppm/localization'
# launcher_dir = os.getcwd()
# cache_dir = f'{os.getcwd()}/devroot/var' # in .gitignore
# config_dir = f'{os.getcwd()}/devroot/etc'
# modules_dir = f'{os.getcwd()}/modules'
# locale_dir = f'{os.getcwd()}/localization'

os.makedirs(cache_dir, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)
os.makedirs(launcher_dir, exist_ok=True)
os.makedirs(locale_dir, exist_ok=True)


init(autoreset=False) # init colorama
sys.setrecursionlimit(1500) 
sys.path.append(launcher_dir) # Add custom path for ppm modules
import modules.dpkg
import modules.init
import modules.lock
import modules.utils

modules.init.config_dir = config_dir
modules.lock.cache_dir = cache_dir
modules.dpkg.cache_dir = cache_dir

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
init         Initialize configuration files and software sources
reset        Force remove ppm process lock
refresh      Synchronize the dpkg database""")



def main():
    if modules.utils.check_is_root() is False:
        # print("Please run ppm as root permissions.")

        path = os.getcwd()
        print(f"{warn} Running ppm as normal user.")
        return_code = os.system(f"sudo bash -c 'cd {path}; /bin/python3 {" ".join(sys.argv)}'") 
        exit() 
    

    
    if len(sys.argv) < 2:
        print(f"{error} Not enough arguments provided.")
        print_help()
        exit()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'init':
        if modules.init.init_repo_config():
            print(f'{success} The configuration file has been initialized.')
    elif command == 'refresh':
        print(f"{info} Refreshing...")
        installed = modules.dpkg.refresh_installed_dpkg()
        print(f"{info} The current system has {installed} packages installed.")
    elif command == 'help':
        print_help()
    elif command == 'reset':
        print(f"{success} Successfully removed the lock file.")
        modules.lock.lock_disable()
    else:
        print(f"{error} Provided command not found.")

if __name__ == "__main__":
    main()
else:
    print(f"{error} Directly importing ppm launcher is not recommend for managing system packages, you should be importing the modules of ppm, not the launcher.")
    print(f"{info} See more infomation at https://ppm.stevesuk.eu.org/importing-launcher")