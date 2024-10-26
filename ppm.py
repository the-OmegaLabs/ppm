#!/bin/python3

import json
import sys
import os
import requests
import lzma
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

version = "alpha-1"
success = f"{Fore.GREEN}::{Fore.RESET}"
get = f"{Fore.CYAN}::{Fore.RESET}"
info = f"{Fore.BLUE}::{Fore.RESET}"
warn = f"{Fore.YELLOW}::{Fore.RESET}"
error = f"{Fore.RED}::{Fore.RESET}"


# Ensure the script is run with root permissions
if os.getuid() != 0:
    print("请以 root 权限运行。")
    sys.exit(1)

# Create cache directory if it doesn't exist
cache_dir = '/var/cache/ppm'
os.makedirs(cache_dir, exist_ok=True)

def init_config():
    os.makedirs('/etc/ppm', exist_ok=True)
    os.chdir('/etc/ppm')


    example_repo = [
        {
            'name': 'OmegaOS Base',
            'type': 'deb',
            'url': 'http://mirrors.ustc.edu.cn/debian',
            'codename': 'stable',
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
    
    print(f"{success} 成功初始化配置文件于 \"/etc/ppm\"")

def update_packages():
    """Update package metadata from the repository."""
    with open('/etc/ppm/repo.json') as f:
        repos = json.load(f)

    for repo in repos:
        if repo['type'] == 'deb':
            print(f"{info} 正在更新软件包列表: {repo['name']}...")
            url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
            response = requests.get(url)

            print(f"{get} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']}")

            with open(f'{cache_dir}/Packages.xz', 'wb') as f:
                f.write(response.content)

            with lzma.open(f'{cache_dir}/Packages.xz') as compressed:
                with open(f'{cache_dir}/Packages.raw', 'wb') as uncompressed:
                    uncompressed.write(compressed.read())

            package_list = parse_packages(f'{cache_dir}/Packages.raw')
            save_packages_to_json(package_list)

            print(f'{success} 所有软件包列表文件已更新。')

def parse_packages(file_path):
    """Parse package information from the raw package file."""
    with open(file_path) as f:
        data = f.read()
    
    packages = data.strip().split('\n\n')
    package_list = []

    for pkg_info in packages:
        package_dict = {}
        for line in pkg_info.strip().split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                package_dict[key] = value.strip()
        package_list.append(package_dict)

    return package_list

def save_packages_to_json(package_list):
    """Save the list of packages to a JSON file."""
    package_json = json.dumps(package_list, ensure_ascii=False, indent=4)
    with open(f'{cache_dir}/Packages.json', 'w') as f:
        f.write(package_json)

def search_package(target):
    """Search for packages in the JSON file that match the target."""
    with open(f'{cache_dir}/Packages.json') as f:
        packages = json.load(f)

    found = 0
    for pkg in packages:
        if target in pkg.get('Package', ''):
            print(pkg['Package'].replace(target, f'{Fore.RED}{target}{Fore.RESET}'))
            found += 1

    if found == 0:
        print(f"{error} 无法使用 '{target}' 关键词找到任何软件包。")
    else:
        print(f'{success} 已找到 {found} 个软件包。')

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print(f"""ppm {version}: 缺失命令
用法: ppm [选项] 命令

ppm 是一个命令行包管理器，目前正在测试。
如果你遇到在使用 ppm 时的任何问题，请反馈到 [https://github.com/Stevesuk0/ppm/issues]。

本软件为自由软件，遵循 GNU Public License 第二版开源协议。

常用命令:
update       更新软件包列表
search       通过关键词检索软件包
download     下载一个软件包与其依赖
init         初始化配置文件、软件源""")
        exit()
    command = sys.argv[1]
    if command in 'update':
        update_packages()
    elif command == 'search' and len(sys.argv) == 3:
        search_package(sys.argv[2])
    elif command == 'version':
        show_version()
    elif command == 'init':
        init_config()
    else:
        print(f"{error} Invalid command or missing arguments.")

def show_version():
    print(f"ppm {version} by @Stevesuk0")
    sys.exit(1)
    

if __name__ == "__main__":
    main()
