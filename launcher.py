#!/usr/bin/python3

import sys
sys.path.append('/opt/ppm') # fix ModuleNotFoundError

from colorama import init, Fore, Style, Back
import os
import modules.dpkg
import modules.init
import modules.lock



init() # init colorama

version = "1.0"
info_character = '<>'

success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

print(f'ppm {version}')

def main():
    print("Hello, World!")


if __name__ == "__main__":
    main()
else:
    print(f"{error} Directly importing ppm is not allowed for managing system packages.")
    print(f"{info} Ideally, you should be importing the modules of ppm, not the launcher.")

