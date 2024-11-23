#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import json
import requests
import lzma

# 傻逼模块化，狗都不做。
# 定义颜色符号。
info_character = '<>'
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"
get = f"{Fore.CYAN}<>{Fore.RESET}"
cache_dir = '/var/cache/ppm'


class manager:
    def __init__(self):
        self.cache_dir = '/var/cache/ppm'
        self.all_packages = self.load_all_packages()

    def parse_packages(self, file_path):
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

    def update_packages(self):
        """Update package metadata from the repository."""
        with open('/etc/ppm/repo.json') as f:
            self.repos = json.load(f)

        for repo in self.repos:
            if repo['type'] == 'deb':
                print(f"{info} Updating package list: {repo['name']} ({repo['type']})...")
                print(
                    f"{info} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages",
                    end='\r')
                url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
                try:
                    self.response = requests.get(url)
                    print(
                        f"{get} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
                except:
                    print(
                        f"{error} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
                path = f"{self.cache_dir}/{repo['name'].lower().replace(' ', '_')}"
                with open(f'{path}.xz', 'wb') as f:
                    f.write(self.response.content)

                print(f"{info} Converting apt package list \"{repo['name']}\" to ppm format.")

                with lzma.open(f'{path}.xz') as compressed:
                    with open(f'{path}.raw', 'wb') as uncompressed:
                        uncompressed.write(compressed.read())

                self.package_list = self.parse_packages(f'{path}.raw')
                self.save_packages_to_json(self.package_list, path)
                print(f"{success} Successfully updated {repo['name']} ({repo['type']}).")

            else:
                print(f"{warn} Unable to parse package source {repo['name']} ({repo['type']}), ignoring this item.")

        print(f'{success} All package list files have been updated.')

    def save_packages_to_json(self, ackage_list, path):
        """Save the list of packages to a JSON file."""
        self.package_json = json.dumps(self.package_list, ensure_ascii=False, indent=4)
        with open(f'{path}.json', 'w') as f:
            f.write(self.package_json)

    def load_all_packages(self):
        # Load all package data once into a dictionary
        self.package_data = {}
        for path in os.listdir('/var/cache/ppm/'):
            try:
                if 'json' in path:
                    with open(f"{self.cache_dir}/omegaos_base.json") as f:
                        packages = json.loads(f.read())
                    self.package_data.update(packages)
            except "FileNotFoundError":
                os.mkdir('/var/cache/ppm/')
        return self.package_data

    def search(self, packname):
        # Directly search in preloaded package data
        for path, package in self.all_packages.items():
            if package.get('Package') == packname:
                return package
        return None

    def download(self, dolist, repo, install=False):
        failed = []
        a = 0
        with open('/var/cache/ppm/status.json') as f:
            installed = json.loads(f.read())
        for i in dolist:
            terminal_size = os.get_terminal_size()
            width = int(terminal_size.columns * 0.5)

            a += 1
            url = f"{repo['url']}/{self.search(i)['Filename']}"
            sys.stdout.write(
                f"{info} ({a}/{len(dolist)}) [{'█' * int((a / len(dolist)) * width)}{int(((len(dolist) - a) / len(dolist)) * width) * ' '}] {i}\r")
            sys.stdout.flush()

            try:
                # if i in installed:
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
                print(
                    f"{get} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {file_size} {iter}")
                with open(f'{i}.dpkg', 'wb') as f:
                    f.write(response.content)
            except:
                print(
                    f"{error} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {response.status_code}")
                failed.append(i)

        print(f"{info} Package download complete.")

        if len(failed) != 0:
            print(f'{warn} {len(failed)} packages failed to download, retrying...')
            a = 0
            for i in failed:
                a += 1
                url = f"{repo['url']}/{self.search(i)['Filename']}"
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
                    print(
                        f"{get} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {file_size} {iter}")
                    with open(f'{i}.dpkg', 'wb') as f:
                        f.write(response.content)
                except:
                    print(
                        f"{error} {a} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} {i} {response.status_code}")

    def download_package(self, dolist):
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
            self.download(dolist, repo)
        else:
            pass

    def install_package(self, dolist):
        os.makedirs('/var/cache/ppm/downloading/', exist_ok=True)
        os.chdir('/var/cache/ppm/downloading/')
        with open('/etc/ppm/repo.json') as f:
            repo = json.loads(f.read())
            repo = repo[0]
        a = 0
        if len(dolist) == 0:
            print(f"{error} Unable to install this package.")
            self.lock_disable()
        print(f"{info} The following new packages will be installed: ", end='')

        for i in dolist:
            print(i, end=' ')
        print()

        choice = input(f"{info} There are {len(dolist)} packages in total, start installing? [Y/n] ")
        if not choice:
            self.download(dolist, repo, install=True)
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

    def get_package(self, packname, depend=None):

        if not packname:
            return None
        if depend is None:
            depend = set()  # Using a set for faster lookups

        if '|' in packname:
            print(f'{warn} Multiple possible dependency choices detected: {packname.replace("|", "or")}.')
            packname = packname.split(' | ')[0]
            print(f'{warn} The default choice will be {packname}.')

        package = self.search(packname)
        if not package or package['Package'] in depend:
            return depend

        depend.append(package['Package'])

        try:
            deps = [dep.split(' (')[0] for dep in package.get('Depends', '').split(', ')]
        except KeyError:
            return depend  # No dependencies found

        for dep in deps:
            if dep not in depend:
                self.get_package(dep, depend)

        return depend

    def sync_dpkg_status(self):
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

    def search_package(self, target):
        """Search for packages in the JSON file that match the target."""
        found = 0

        with open(f"{self.cache_dir}/omegaos_base.json") as f:
            packages = json.loads(f.read())
        for pkg in packages:
            if target in packages[pkg].get('Package', ''):
                print(packages[pkg]['Package'].replace(target, f'{Fore.RED}{target}{Fore.RESET}'))
                found += 1

        if found == 0:
            print(f"{error} No package found using the '{target}' keyword.")
        else:
            print(f'{success} {found} packages found.')

    """New Features by bigdickbzym2🍥🍥🍥🍥"""

    def switch_repo(self, repo):
        if (os.path.exists("/etc/ppm/repo.json") == false):
            print(
                f"{error} you haven't created the repo file, plz run 'ppm init' to create the repo file and initiaze ppm")
        else:
            changed_repo = [
                {
                    'name': 'OmegaOS Base',
                    'type': 'deb',
                    'url': f'https://{repo}/debian/',
                    'codename': 'testing',
                    'category': 'main/binary-amd64',
                },
                {
                    'name': 'OmegaOS Extra(omg this is fucking useless i want to delete this fucking repo)',
                    'type': 'ppm',
                    'url': 'http://ppm.stevesuk.eu.org/omegaos',
                    'codename': 'sunset',
                },
            ]
            with open('/etc/ppm/repo.json', 'w') as f:
                f.write(json.dumps(changed_repo, indent=4, ensure_ascii=False))


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
        return os.popen("whoami") == "root"

    def init(self):
        os.makedirs('/etc/ppm', exist_ok=True)
        os.chdir('/etc/ppm')

        example_repo = [
            {
                'name': 'OmegaOS Base',
                'type': 'deb',
                'url': 'https://ftp.debian.org/debian/',
                'codename': 'testing',
                'category': 'main/binary-amd64',
            },
            {
                'name': 'OmegaOS Extra(omg this is fucking useless i want to delete this fucking repo)',
                'type': 'ppm',
                'url': 'http://ppm.stevesuk.eu.org/omegaos',
                'codename': 'sunset',
            },
        ]

        with open('repo.json', 'w') as f:
            f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))

        print(f"{success} Successfully initialized the configuration file at \"/etc/ppm/\"")

    def get_status(self):
        with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f:  # 强大的傻逼查询，脑残但是高效。
            a = f.read().strip().split(',')
            installed = {}

            for i in a:
                parts = i.split('/')
                if len(parts) == 2 and parts[1]:
                    installed[parts[0]] = parts[1]

            return installed


# 模块对象
Module = modules()
Manager = manager()

# version = "1.0"
# launcher_dir = '/opt/ppm'
# cache_dir = '/var/cache/ppm'
# config_dir = '/etc/ppm'
# modules_dir = '/opt/ppm/modules'
# locale_dir = '/opt/ppm/localization'
version = "1.1"
launcher_dir = '.'
config_dir = '/etc/ppm'

# 世界上最强大的系统检测
if (sys.platform.startswith('win32')):
    print(f"{error} 你都用包管理器了还鸡巴用windows。操你妈滚回家去吧")
    exit(1)
else:
    pass

init(autoreset=False)  # colorama初始化
sys.setrecursionlimit(1500)

print(f'ppm {version}')


def show_version():
    print(f"ppm alpha {version} by @bzym2 and @stevesuk0")


def main():
    if Module.root_check() is False:
        path = os.getcwd()
        print(f"{warn} Running ppm as normal user.")
        args = " ".join(sys.argv)
        return_code = os.system(f"pkexec bash -c 'cd {path}; {args}'")
        if return_code != 256:
            print(f"{error} Can't running ppm as root.")
    else:
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
            Manager.update_packages()
            Manager.sync_dpkg_status()
        elif command == 'search' and len(sys.argv) == 3:
            Manager.search_package(sys.argv[2])
        elif command == 'version':
            show_version()
        elif command == 'init':
            Module.init()
        elif command == 'syncdpkg':
            Manager.sync_dpkg_status()
        elif command == 'reset':
            Module.lock_disable()
        elif command == 'download' and len(sys.argv) == 3:
            if Module.lock_check():
                print(f"{error} Unable to lock the database: file already exists")
                print(f"{error} If you are sure ppm is not running, please delete '/var/cache/ppm/ppm.lck'.")
                exit()
            Module.lock_enable()
            dolist = Manager.get_package(sys.argv[2], [])
            Manager.download_package(dolist)
            Module.lock_disable()
        elif command == 'install' and len(sys.argv) == 3:
            if Module.lock_check():
                print(f"{error} Unable to lock the database: file already exists")
                print(f"{error} If you are sure ppm is not running, please delete '/var/cache/ppm/ppm.lck'.")
                exit()
            Module.lock_enable()
            dolist = Manager.get_package(sys.argv[2], [])
            Manager.install_package(dolist)
            Manager.sync_dpkg_status()
            Module.lock_disable()
        elif command == 'switchrepo' and len(sys.argv) == 3:
            Manager.switch_repo(sys.argv[2])
        else:
            print(f"{error} Invalid command or missing arguments.")


if __name__ == "__main__":
    main()
else:
    print(f"{error} Directly importing ppm is not allowed for managing system packages.")
    print(f"{info} Ideally, you should be importing the modules of ppm, not the launcher.")