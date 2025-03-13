from utils.pColor import pColor
import ppmcore
import locale

"""
    ppm personalized configuration file
    This file is used to store all the configurations for the ppm launcher.
    Such as the version, directories, output style, and the language, etc. 
    Modify this file if you want!
"""


""" Personalize Config """
# Language:
# Auto Detect default locale
language = locale.getdefaultlocale()[0]
# language = "en_US"
# ↑ you can do that either
# Available languages: en_US, zh_CN, ru_RU, en_WW
# Please contribute to the localization if you can!

# print version:
print_version = False
# If you want to print the version of ppm when it starts, set this to True.

# Output Style:
info_character = '<>'
enable_color_output = ppmcore.isColorSupported()

success = f"{pColor.GREEN}{info_character}{pColor.RESET}"
info = f"{pColor.BLUE}{info_character}{pColor.RESET}"
warn = f"{pColor.YELLOW}{info_character}{pColor.RESET}"
error = f"{pColor.RED}{info_character}{pColor.RESET}"

success_alt = f"DONE:"
info_alt = f"INFO:"
warn_alt = f"WARN:"
error_alt = f"FAIL:"

# Don't change these unless you know what you are doing!
""" Basic Config """
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = f'{launcher_dir}/localization'

