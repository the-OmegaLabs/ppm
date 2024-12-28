from utils.pColor import pColor
import modules.verify

"""
    PPM Configuration File
    Modify this file as your please XD
"""

""" Basic Config """
version = "0.3"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = f'{launcher_dir}/localization'

""" Personalize Config """
language = 'en_US'
info_character = '<>'
print_version = False
enable_color = modules.verify.is_color_supported()
success = f"{pColor.GREEN}{info_character}{pColor.RESET}"
info = f"{pColor.BLUE}{info_character}{pColor.RESET}"
warn = f"{pColor.YELLOW}{info_character}{pColor.RESET}"
error = f"{pColor.RED}{info_character}{pColor.RESET}"
success2 = f"{pColor.BOLD}DONE{pColor.RESET}"
info2 = f"{pColor.BOLD}INFO{pColor.RESET}"
warn2 = f"{pColor.BOLD}WARN{pColor.RESET}"
error2 = f"{pColor.BOLD}FAIL{pColor.RESET}"
