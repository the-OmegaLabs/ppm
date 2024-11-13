#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import json

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
        with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f: # 强大的傻逼查询，脑残但是高效。
            a = f.read().strip().split(',')
            installed = {}
            
            for i in a:
                parts = i.split('/')
                if len(parts) == 2 and parts[1]: 
                    installed[parts[0]] = parts[1]
            
            return installed
        
# 模块对象
Module = modules()

# 定义颜色符号。
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

# 世界上最强大的系统检测
if(sys.platform.startswith('win32')):
    print(f"{error} 你都用包管理器了还鸡巴用windows。操你妈滚回家去吧")
    exit(1)
else:
    pass

init(autoreset=False) # colorama初始化
sys.setrecursionlimit(1500)

print(f'ppm {version}')

def print_help():
    """
    打印傻逼帮助信息。
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
        path = os.getcwd()
        print(f"{warn} Running ppm as normal user.")
        args = " ".join(sys.argv)
        return_code = os.system(f"pkexec bash -c 'cd {path}; {args}'")
        if return_code != 256:
            print(f"{error} Can't running ppm as root.")
        exit()

    # 检查有没有足够的傻逼参数。
    if len(sys.argv) < 2:
        print(f"{error} Not enough arguments provided.")
        print_help()
        exit(1) # 如果没就跟用户爆了。
    else:
        print(f"{success} Command line arguments are sufficient.")

if __name__ == "__main__":
    main()
else:
    print(f"{error} Directly importing ppm is not allowed for managing system packages.")
    print(f"{info} Ideally, you should be importing the modules of ppm, not the launcher.")
