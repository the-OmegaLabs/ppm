from utils.pColor import pColor
import modules.verify

"""
    ppm personilized configuration file
    This file is used to store all the configurations for the ppm launcher.
    Such as the version, directories, output style, and the language, etc. 
    Modify this file if you want!
"""


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
enable_color_output = modules.verify.is_color_supported()

success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

success_alt = f"DONE:"
info_alt = f"INFO:"
warn_alt = f"WARN:"
error_alt = f"FAIL:"

# Don't change these unless you know what you are doing!
""" Basic Config """
version = "0.3"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = f'{launcher_dir}/localization'

