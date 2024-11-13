#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import json
import platform

# 傻逼模块化，狗都不做。
class modules:
    def lock_disable(self):
            try:
                os.remove('/var/cache/ppm/lock')
                return True
            except:
                return False

    def lock_enable(self):
        with open('/var/cache/ppm/lock', 'w') as f:
            f.write('')

    def lock_check(self):
        return os.path.exists('/var/cache/ppm/ppm.lck')
    
    def root_check(self):
        return os.popen("whoami")=="root"
    
    def init(self):
        os.makedirs('/etc/ppm', exist_ok=True)
        os.chdir('/etc/ppm')

        example_repo = [
            {
                'name': 'OmegaOS Base',
                'type': 'deb',
                'url': 'http://mirrors.ustc.edu.cn/debian',
                'codename': 'testing',
                'category': 'main/binary-amd64',
            },
            {
                'name': 'OmegaOS Extra',
                'type': 'ppm',
                'url':  'http://ppm.stevesuk.eu.org/omegaos',
                'codename': 'sunset',
            },
        ]

        with open('repo.json', 'w') as f:
            f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))
        
        return True
    
    def get_status(self):
        with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f: # retrieving dpkg information using dpkg-query
            a = f.read().strip().split(',')
            installed = {}
            
            for i in a:
                parts = i.split('/')
                if len(parts) == 2 and parts[1]: 
                    installed[parts[0]] = parts[1]
            
            return installed
        
# 模块对象
Module = modules()

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

# 世界上最强大的系统检测
if(platform.system=="Windows"):
    print(f"{error} 你都用包管理器了还鸡巴用windows。操你妈滚回家去吧")
else:
    pass

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
    if Module.root_check() is False:
        # print("Please run ppm as root permissions.")
        
        
        path = os.getcwd()
        print(f"{warn} Running ppm as normal user.")
        args = " ".join(sys.argv)
        return_code = os.system(f"pkexec bash -c 'cd {path}; {args}'")
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
