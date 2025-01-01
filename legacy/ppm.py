#!/bin/python3

import json
import sys
import os
import requests
import lzma
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

version = "beta-2"
success = f"{Fore.GREEN}<>{Fore.RESET}"
get = f"{Fore.CYAN}<>{Fore.RESET}"
info = f"{Fore.BLUE}<>{Fore.RESET}"
warn = f"{Fore.YELLOW}<>{Fore.RESET}"
error = f"{Fore.RED}<>{Fore.RESET}"

sys.setrecursionlimit(2000)

# 全局缓存
dependency_cache = {}


# Ensure the script is run with root permissions
if os.getuid() != 0:
    print("Please run with root permissions.")
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
            'url': 'http://mirrors.ustppmcore..edu.cn/debian',
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
    
    print(f"{success} Successfully initialized the configuration file at \"/etc/ppm/\"")

def update_packages():
    """Update package metadata from the repository."""
    with open('/etc/ppm/repo.json') as f:
        repos = json.load(f)

    for repo in repos:
        if repo['type'] == 'deb':
            print(f"{info} Updating package list: {repo['name']} ({repo['type']})...")
            print(f"{info} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages", end='\r')
            url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
            try:
                response = requests.get(url)
                print(f"{get} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
            except:
                print(f"{error} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
            path = f"{cache_dir}/{repo['name'].lower().replace(' ', '_')}"
            with open(f'{path}.xz', 'wb') as f:
                f.write(response.content)

            print(f"{info} Converting apt package list \"{repo['name']}\" to ppm format.")


            with lzma.open(f'{path}.xz') as compressed:
                with open(f'{path}.raw', 'wb') as uncompressed:
                    uncompressed.write(compressed.read())

            package_list = parse_packages(f'{path}.raw')
            save_packages_to_json(package_list, path)
            print(f"{success} Successfully updated {repo['name']} ({repo['type']}).")
            
        else:
            print(f"{warn} Unable to parse package source {repo['name']} ({repo['type']}), ignoring this item.")

    print(f'{success} All package list files have been updated.')


def parse_packages(file_path):
    """Parse package information from the raw package file."""
    with open(file_path) as f:
        data = f.read()
    
    packages = data.strip().split('\n\n')
    packages_dicts = {}

    for pkg_info in packages:
        package_dict = {}
        for line in pkg_info.strip().split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                package_dict[key] = value.strip()
        
        package_name = package_dict.get("Package", "unknown_package")
        packages_dicts[package_name] = package_dict

    return packages_dicts


def save_packages_to_json(package_list, path):
    """Save the list of packages to a JSON file."""
    package_json = json.dumps(package_list, ensure_ascii=False, indent=4)
    with open(f'{path}.json', 'w') as f:
        f.write(package_json)

def load_all_packages():
    # Load all package data once into a dictionary
    package_data = {}
    for path in os.listdir('/var/cache/ppm/'):
        if 'json' in path:
            with open(f"{cache_dir}/omegaos_base.json") as f:
                packages = json.loads(f.read())
            package_data.update(packages)
    return package_data

all_packages = load_all_packages()

def search(packname):
    # Directly search in preloaded package data
    for path, package in all_packages.items():
        if package.get('Package') == packname:
            return package
    return None

def download(dolist, repo, install = False):
    failed = []
    a = 0
    with open('/var/cache/ppm/status.json') as f:
        installed = json.loads(f.read())
    for i in dolist:
        terminal_size = os.get_terminal_size() 
        width = int(terminal_size.columns * 0.5)
        
        a += 1
        url = f"{repo['url']}/{search(i)['Filename']}"
        sys.stdout.write(f"{info} ({a}/{len(dolist)}) [{'█' * int((a / len(dolist)) * width)}{int(((len(dolist) - a) / len(dolist)) * width) * ' '}] {i}\r")
        sys.stdout.flush()
        
        try:    
            #if i in installed:
            #    continue
            response = requests.get(url)    
            file_size = float(response.headers.get('Content-Length')) / 1024
            iter = 'KB'
            if file_size > 1024:
                file_size = round(file_size / 1024, 2)
                iter = 'MB'
            else:
                file_size = round(file_size, 2)
            print(f"{' ' * width * 2}", end='\r')
            print(f"{get} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {file_size} {iter}")
            with open(f'{i}.dpkg', 'wb') as f:
                f.write(response.content)
        except:
            print(f"{error} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {response.status_code}")
            failed.append(i)
    
    print(f"{info} Package download complete.")

    
    if len(failed) != 0:
        print(f'{warn} {len(failed)} packages failed to download, retrying...')
        a = 0
        for i in failed:
            a += 1
            url = f"{repo['url']}/{search(i)['Filename']}"
            sys.stdout.write(f"{warn} Retry: ({a}/{len(failed)}) {i}\r")
            sys.stdout.flush()
            failed = []
            try:    
                response = requests.get(url)    
                file_size = float(response.headers.get('Content-Length')) / 1024
                iter = 'KB'
                if file_size > 1024:
                    file_size = round(file_size / 1024, 2)
                    iter = 'MB'
                else:
                    file_size = round(file_size, 2)
                print(f"{' ' * width * 2}", end='\r')
                print(f"{get} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {file_size} {iter}")
                with open(f'{i}.dpkg', 'wb') as f:
                    f.write(response.content)
            except:
                print(f"{error} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {response.status_code}")

def download_package(dolist):
    os.makedirs('/var/cache/ppm/downloading/', exist_ok=True)
    with open('/etc/ppm/repo.json') as f:
        repo = json.loads(f.read())
        repo = repo[0]
    print(f"The following new packages will be downloaded: ", end='')
    for i in dolist:
        print(i, end=' ')
    print()
    choice = input(f"There are {len(dolist)} packages in total, start downloading? [Y/n] ")
    if not choice:
        download(dolist, repo)
    else:
        pass

def install_package(dolist):
    os.makedirs('/var/cache/ppm/downloading/', exist_ok=True)
    os.chdir('/var/cache/ppm/downloading/')
    with open('/etc/ppm/repo.json') as f:
        repo = json.loads(f.read())
        repo = repo[0]
    a = 0
    if len(dolist) == 0:
        print(f"{error} Unable to install this package.")
        lock_disable()
    print(f"{info} The following new packages will be installed: ", end='')

    for i in dolist:
        print(i, end=' ')
    print()
    
    choice = input(f"{info} There are {len(dolist)} packages in total, start installing? [Y/n] ")
    if not choice:
        download(dolist, repo, install = True)
    else:
        return 0
    

    
    countdeb = 0
    for i in os.listdir():
        if '.dpkg' in i:
            countdeb += 1
    print(f'{info} {countdeb} Debian packages found, invoking dpkg...')
    os.system('apt install --fix-broken -y')
    os.system(f'dpkg -i *')
    print(f"{info} Cleaning up...")
    for i in os.listdir():
        os.remove(i)


def get_package(packname, depend=None):

    if not packname:
        return None
    if depend is None:
        depend = set()  # Using a set for faster lookups
    
    if '|' in packname:
        print(f'{warn} Multiple possible dependency choices detected: {packname.replace("|", "or")}.')
        packname = packname.split(' | ')[0]
        print(f'{warn} The default choice will be {packname}.')
    
    package = search(packname)
    if not package or package['Package'] in depend:
        return depend
    
    depend.append(package['Package'])
    
    try:
        deps = [dep.split(' (')[0] for dep in package.get('Depends', '').split(', ')]
    except KeyError:
        return depend  # No dependencies found
    
    for dep in deps:
        if dep not in depend:
            get_package(dep, depend)
    
    return depend


def search_package(target):
    """Search for packages in the JSON file that match the target."""
    found = 0

    with open(f"{cache_dir}/omegaos_base.json") as f:
        packages = json.loads(f.read())
    for pkg in packages:
        if target in packages[pkg].get('Package', ''):
            print(packages[pkg]['Package'].replace(target, f'{Fore.RED}{target}{Fore.RESET}'))
            found += 1

    if found == 0:
        print(f"{error} No package found using the '{target}' keyword.")
    else:
        print(f'{success} {found} packages found.')

def sync_dpkg_status():
    print(f"{info} Synchronizing the status of already installed dpkg packages...")
    
    with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f:
        a = f.read().strip().split(',')
        dic = {}
        
        for i in a:
            parts = i.split('/')
            if len(parts) == 2 and parts[1]: 
                dic[parts[0]] = parts[1]
        
        # 确保目标目录存在
        os.makedirs('/var/cache/ppm', exist_ok=True)
        
        with open('/var/cache/ppm/status.json', 'w') as f:
            f.write(json.dumps(dic, indent=4, ensure_ascii=False))
    
    print(f"{info} The current system has {len(dic)} packages installed.")
    

def lock_disable():
    os.remove('/var/cache/ppm/ppm.lck')

def lock_enable():
    with open('/var/cache/ppm/ppm.lck', 'w') as f:
        f.write('')

def lock_check():
    return os.path.exists('/var/cache/ppm/ppm.lck')

def main():
    """Main function to handle command-line arguments."""
    if not os.path.exists('/etc/ppm'):
        init_config()
    sys.setrecursionlimit(2000)
    if len(sys.argv) < 2:
        print(f"""ppm {version}: Missing command
Usage: ppm [options] command

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at [https://github.com/Stevesuk0/ppm/issues].

This software is free and follows the GNU General Public License v2.

Common commands:
update       Update the package list
search       Search for packages by keyword
download     Download a package and its dependencies
install      Install a package and its dependencies
init         Initialize configuration files and software sources
reset        Force remove ppm process lock
syncdpkg     Synchronize the status of installed packages from dpkg""")
        exit()
    command = sys.argv[1]
    if command in 'update':
        update_packages()
        sync_dpkg_status()
    elif command == 'search' and len(sys.argv) == 3:
        search_package(sys.argv[2])
    elif command == 'version':
        show_version()
    elif command == 'init':
        init_config()
    elif command == 'syncdpkg':
        sync_dpkg_status()
    elif command == 'reset':
        lock_disable()
    elif command == 'download' and len(sys.argv) == 3:
        if lock_check():
            print(f"{error} Unable to lock the database: file already exists")
            print(f"{error} If you are sure ppm is not running, please delete '/var/cache/ppm/ppm.lck'.")
            exit()
        lock_enable()
        dolist = get_package(sys.argv[2], [])
        download_package(dolist)
        lock_disable()
    elif command == 'install' and len(sys.argv) == 3:
        if lock_check():
            print(f"{error} Unable to lock the database: file already exists")
            print(f"{error} If you are sure ppm is not running, please delete '/var/cache/ppm/ppm.lck'.")
            exit()
        lock_enable()
        dolist = get_package(sys.argv[2], [])
        install_package(dolist)
        sync_dpkg_status()
        lock_disable()
    else:
        print(f"{error} Invalid command or missing arguments.")


def show_version():
    print(f"ppm {version} by @Stevesuk0")
    sys.exit(1)
    

if __name__ == "__main__":
    main()