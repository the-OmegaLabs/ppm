from colorama import *
"""
    PPM Configuration File
    Modify this file as your please XD
"""

init(autoreset=False)

""" Basic Config """
version = "0.2"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = f'{launcher_dir}/localization'

""" Personalize Config """
language = 'en_US'
info_character = '##' # I think <> is better LOL
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"