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
    print("Please run with root permission")
    sys.exit(1)

# Create cache directory if it doesn't exist
cache_dir = '/var/cache/ppm'
os.makedirs(cache_dir, exist_ok=True)

def update_packages():
    """Update package metadata from the repository."""
    with open('/etc/ppm/repo.json') as f:
        repos = json.load(f)

    for repo in repos:
        if repo['type'] == 'deb':
            print(f"{info} Updating package metadata: {repo['name']}...")
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

            print(f'{success} All sources are up-to-date.')

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
        print(f"{error} No package found matching '{target}'.")
    else:
        print(f'success')

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("""ppm: Command help
update       Update package metadata from the repositories
search       Search for a package by name""")

        sys.exit(1)

    command = sys.argv[1]
    if command == 'update':
        update_packages()
    elif command == 'search' and len(sys.argv) == 3:
        search_package(sys.argv[2])
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()
