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
    
    print(f"{success} 成功初始化配置文件于 \"/etc/ppm/\"")

def update_packages():
    """Update package metadata from the repository."""
    with open('/etc/ppm/repo.json') as f:
        repos = json.load(f)

    for repo in repos:
        if repo['type'] == 'deb':
            print(f"{info} 正在更新软件包列表: {repo['name']} ({repo['type']})...")
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

            print(f"{info} 正在将 apt 软件包列表 \"{repo['name']}\" 转换为 ppm 格式。")

            with lzma.open(f'{path}.xz') as compressed:
                with open(f'{path}.raw', 'wb') as uncompressed:
                    uncompressed.write(compressed.read())

            package_list = parse_packages(f'{path}.raw')
            save_packages_to_json(package_list, path)
            print(f"{success} 成功更新 {repo['name']} ({repo['type']})。")
            
        else:
            print(f"{warn} 无法解析软件包源 {repo['name']} ({repo['type']})，忽略该项。")

    print(f'{success} 所有软件包列表文件已更新。')

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
    terminal_size = os.get_terminal_size() 
    width = int(terminal_size.columns * 0.5)
    failed = []
    a = 0
    with open('/var/cache/ppm/status.json') as f:
        installed = json.loads(f.read())
    for i in dolist:
        a += 1
        url = f"{repo['url']}/{search(i)['Filename']}"
        sys.stdout.write(f"{info} ({a}/{len(dolist)}) [{'=' * int((a / len(dolist)) * width)}>{int(((len(dolist) - a) / len(dolist)) * width) * ' '}] {i}\r")
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
    
    print(f"{info} 软件包下载完毕。")
    
    if len(failed) != 0:
        print(f'{warn} 有 {len(failed)} 个软件包安装失败，正在重试...')
        a = 0
        for i in failed:
            a += 1
            url = f"{repo['url']}/{search(i)['Filename']}"
            sys.stdout.write(f"{warn} 修复中：({a}/{len(failed)}) {i}\r")
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
    a = 0
    print(f"以下新软件包将被下载：", end='')
    for i in dolist:
        print(i, end=' ')
    print()
    choice = input(f"共 {len(dolist)} 个软件包，开始下载？[Y/n] ")
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
        print(f"{error} 无法安装此软件包。")
        exit()
    print(f"{info} 以下新软件包将被安装：", end='')
    for i in dolist:
        print(i, end=' ')
    print()
    
    choice = input(f"{info} 共 {len(dolist)} 个软件包，开始安装？[Y/n] ")
    if not choice:
        download(dolist, repo, install = True)
    else:
        return 0
    

    
    countdeb = 0
    for i in os.listdir():
        if '.dpkg' in i:
            countdeb += 1
    print(f'{info} 已发现 {countdeb} 个 Debian 软件包，正在调用 dpkg...')
    os.system('apt install --fix-broken -y')
    os.system(f'dpkg -i *')
    print(f"{info} 正在清理...")
    for i in os.listdir():
        os.remove(i)

def get_package(packname, depend=None):

    if not packname:
        return None
    if depend is None:
        depend = set()  # Using a set for faster lookups
    
    if '|' in packname:
        print(f'{warn} 检测到依赖选择的多重可能性: {packname.replace("|", "或")}。')
        packname = packname.split(' | ')[0]
        print(f'{warn} 将默认选择 {packname}。')
    
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
        print(f"{error} 无法使用 '{target}' 关键词找到任何软件包。")
    else:
        print(f'{success} 已找到 {found} 个软件包。')

def sync_dpkg_status():
    print(f"{info} 正在同步 dpkg 已经安装的软件包状态...")
    
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
    
    print(f"{info} 当前系统已经安装 {len(dic)} 个软件包。")
    

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
        print(f"""ppm {version}: 缺失命令
用法: ppm [选项] 命令

ppm 是一个命令行包管理器，目前正在测试。
如果你遇到在使用 ppm 时的任何问题，请反馈到 [https://github.com/Stevesuk0/ppm/issues]。

本软件为自由软件，遵循 GNU Public License 第二版开源协议。

常用命令:
update       更新软件包列表
search       通过关键词检索软件包
download     下载一个软件包与其依赖
install      安装一个软件包与其依赖
init         初始化配置文件、软件源
reset        强制删除 ppm 进程锁
syncdpkg     从 dpkg 同步已经安装软件包的状态""")
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
            print(f"{error} 无法锁定数据库：文件已存在")
            print(f"{error} 如果你确认 ppm 没有在运行，请删除 '/var/cache/ppm/ppm.lck'。")
            exit()
        lock_enable()
        dolist = get_package(sys.argv[2], [])
        download_package(dolist)
        lock_disable()
    elif command == 'install' and len(sys.argv) == 3:
        if lock_check():
            print(f"{error} 无法锁定数据库：文件已存在")
            print(f"{error} 如果你确认 ppm 没有在运行，请删除 '/var/cache/ppm/ppm.lck'。")
            exit()
        lock_enable()
        dolist = get_package(sys.argv[2], [])
        install_package(dolist)
        sync_dpkg_status()
        lock_disable()
    else:
        print(f"{error} 无效命令或缺失参数。")

def show_version():
    print(f"ppm {version} by @Stevesuk0")
    sys.exit(1)
    

if __name__ == "__main__":
    main()
