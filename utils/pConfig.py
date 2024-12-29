from colorama import *

"""
    ppm personilized configuration file
    This file is used to store all the configurations for the ppm launcher.
    Such as the version, directories, output style, and the language, etc. 
    Modify this file if you want!
"""

init(autoreset=False)

""" Personalize Config """
# Language:
language = 'en_US' 
# Avaliable languages: en_US, zh_CN.
# Please contribute to the localization if you can!

# print version:
print_version = False
# If you want to print the version of ppm when it starts, set this to True.

# Output Style:
info_character = '<>'
enable_color_output = True

success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

success_alt = f"DONE:"
info_alt = f"INFO:"
warn_alt = f"WARN:"
error_alt = f"FAIL:"


""" Directory Config """
# Don't change these unless you know what you are doing!
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = f'{launcher_dir}/localization'