#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import json
import requests
import lzma

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
        self.width = None
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
                print(f"{info} 更新包列表: {repo['name']} ({repo['type']})...")
                print(
                    f"{info} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} 包列表",
                    end='\r')
                url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
                try:
                    self.response = requests.get(url)
                    print(
                        f"{get} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} 包列表")
                except:
                    print(
                        f"{error} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} 包列表")
                path = f"{self.cache_dir}/{repo['name'].lower().replace(' ', '_')}"
                with open(f'{path}.xz', 'wb') as f:
                    f.write(self.response.content)

                print(f"{info} 将APT包列表 \"{repo['name']}\" 转换为PPM格式。")

                with lzma.open(f'{path}.xz') as compressed:
                    with open(f'{path}.raw', 'wb') as uncompressed:
                        uncompressed.write(compressed.read())

                self.package_list = self.parse_packages(f'{path}.raw')
                self.save_packages_to_json(self.package_list, path)
                print(f"{success} 成功更新 {repo['name']} ({repo['type']}).")

            else:
                print(f"{warn} 无法解析源 {repo['name']} ({repo['type']}), 忽略此项。")

        print(f'{success} 所有包列表文件已更新。')

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
            self.width = width
            a += 1
            url = f"{repo['url']}/{self.search(i)['Filename']}"
            sys.stdout.write(
                f"{info} ({a}/{len(dolist)}) [{'█' * int((a / len(dolist)) * width)}{int(((len(dolist) - a) / len(dolist)) * width) * ' '}] {i}\r")
            sys.stdout.flush()

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
                failed.append(i)

        print(f"{info} 包下载完成。")

        if len(failed) != 0:
            print(f'{warn} {len(failed)} 个包下载失败，重试中...')
            a = 0
            for i in failed:
                a += 1
                url = f"{repo['url']}/{self.search(i)['Filename']}"
                sys.stdout.write(f"{warn} 重试: ({a}/{len(failed)}) {i}\r")
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
        print(f"以下新包将被下载: ", end='')
        for i in dolist:
            print(i, end=' ')
        print()
        choice = input(f"共有 {len(dolist)} 个包，开始下载吗? [Y/n] ")
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
            print(f"{error} 无法安装此包。")
            self.lock_disable()
        print(f"{info} 以下新包将被安装: ", end='')

        for i in dolist:
            print(i, end=' ')
        print()

        choice = input(f"{info} 共有 {len(dolist)} 个包，开始安装吗? [Y/n] ")
        if not choice:
            self.download(dolist, repo, install=True)
        else:
            return 0

        countdeb = 0
        for i in os.listdir():
            if '.dpkg' in i:
                countdeb += 1
        print(f'{info} 找到 {countdeb} 个 Debian 包，正在调用 dpkg...')
        print(f'{info} 安装中，请稍等...')

        for i in os.listdir():
            if '.dpkg' in i:
                a += 1
                sys.stdout.write(f"{info} ({a}/{countdeb}) [{'█' * int((a / countdeb) * self.width)}{int(((countdeb - a) / countdeb) * self.width) * ' '}] {i}\r")
                sys.stdout.flush()
                try:
                    os.system(f'dpkg -i {i}')
                except:
                    pass
        print(f'{info} 安装完成。')

    def uninstall_package(self, dolist):
        os.makedirs('/var/cache/ppm/downloading/', exist_ok=True)
        a = 0
        print(f'{info} 以下包将被卸载: ', end='')
        for i in dolist:
            print(i, end=' ')
        print()

        choice = input(f"{info} 确认卸载 {len(dolist)} 个包吗? [Y/n] ")
        if not choice:
            for i in dolist:
                os.system(f'apt-get remove {i}')
                a += 1
                sys.stdout.write(
                    f"{info} ({a}/{len(dolist)}) [{'█' * int((a / len(dolist)) * self.width)}{int(((len(dolist) - a) / len(dolist)) * self.width) * ' '}] {i}\r")
                sys.stdout.flush()
            print(f"{info} 卸载完成。")
        else:
            pass


if __name__ == "__main__":
    init(autoreset=True)
    PPM = manager()
    PPM.update_packages()
