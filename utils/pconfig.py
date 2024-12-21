import colorama as CA
"""
    PPM Configuration File
    Modify this file as your please XD
"""

""" Basic Config """
version = "0.2"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = '/opt/ppm/localization'

""" Personalize Config """
language = 'en_us'
info_character = '##' # I think <> is better LOL
success = f"{CA.Fore.GREEN}{info_character}{CA.Fore.RESET}"
info = f"{CA.Fore.BLUE}{info_character}{CA.Fore.RESET}"
warn = f"{CA.Fore.YELLOW}{info_character}{CA.Fore.RESET}"
error = f"{CA.Fore.RED}{info_character}{CA.Fore.RESET}"