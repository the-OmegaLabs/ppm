#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import utils.pconfig as P

init(autoreset=False) # init colorama
sys.setrecursionlimit(1500)

# Define different message types with colored formatting
success = P.success
info = P.info
warn = P.warn
error = P.error

os.makedirs(P.cache_dir, exist_ok=True)
os.makedirs(P.config_dir, exist_ok=True)
os.makedirs(P.launcher_dir, exist_ok=True)
os.makedirs(P.locale_dir, exist_ok=True)

sys.path.append(P.launcher_dir) # Add custom path for ppm modules

# import modules
import modules
import modules.auth
import modules.managing
import modules.config
import modules.lock

# sync modules config with pconfig
modules.lock.cache_dir = P.cache_dir
modules.managing.cache_dir = P.cache_dir
modules.managing.config_dir = P.config_dir
modules.config.cache_dir = P.cache_dir
modules.config.config_dir = P.config_dir

# print(f'ppm {P.version}')

help_text = """
Usage: ppm [options] command

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at [https://github.com/Stevesuk0/ppm/issues].

This software is free and follows the GNU General Public License v2.

Common commands:
init         Initialize configuration files and software sources
reset        Force remove ppm process lock
refresh      Synchronize the dpkg database
update       Update the package list
search       Search a packages by keyword
clean        Clean ppm cache files"""

def main():
    if len(sys.argv) < 2:
        print(f"{error} Not enough arguments provided.")
        print(help_text)
        exit()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'init':
        if modules.config.initRepoConfig():
            print(f'{success} The configuration file has been initialized.')
    
    elif command == 'download':
        repolist = modules.config.getRepofromCache() 
        for repo in repolist:
            modules.managing.loadPackages(repo) # precaching
            for package_name in args:
                packinfo = modules.managing.downloadPackage(package_name)
                for i in packinfo:
                    print(i)

    elif command == 'search':
        repolist = modules.config.getRepofromCache() 
        for repo in repolist:
            modules.managing.loadPackages(repo) # precaching
            for package_name in args:
                packinfo = modules.managing.searchPackage(package_name)
                if packinfo:
                    homepage = ''
                    if not packinfo.get('Homepage', None) is None:
                        homepage = f"\n      See more infomation at: {packinfo['Homepage']}"
                    print(f"{success} {repo['name']}: {packinfo['Package']}, Version {packinfo['Version']}\n   by {packinfo['Maintainer']}\n      {packinfo['Description']}{homepage}")
                else:
                    print(f"{error} Package \"{package_name}\" not found")

    elif command == 'clean':
        cleaning = modules.config.cleanCacheFolder()
        if cleaning[0]: # bool
            if cleaning[1] == 0:
                print(f"{info} Nothing to clean.") 
            else:
                print(f"{success} Successfully clean {cleaning[1]} caches.")
        else:
            print(f"{error} Failed to clean cache files.")

    elif command == 'refresh':
        print(f"{info} Refreshing...")
        installed = modules.managing.dpkg_refreshInstalled()
        print(f"{info} The current system has {installed} dpkg packages.")

    elif command == 'help':
        print(help_text)

    elif command == 'update':
        repos = modules.config.getRepofromConfiguation()
        for repo in repos:
            print(f"{info} Updating package list: {repo['name']} ({repo['type']})...", end='')
            sys.stdout.flush()
            if modules.managing.updateMetadata(repo)[0]:
                print(f"\r{success} Updated package list: {repo['name']} ({repo['type']})...")
            else:
                print(f"\r{warn} Unable to parse repo \"{repo['name']} ({repo['type']})\"")

    elif command == 'reset':
        if modules.lock.disable():
            print(f"{success} Successfully removed the lock file.")
        else:
            print(f"{error} Failed to remove the lock file.")

    elif command == 'version':
        print(f"{info} ppm {P.version}")
    else:
        print(f"{error} Provided command not found.")

if __name__ == "__main__":
    if modules.auth.checkIsRoot() is False:
        print(f"{warn} Running ppm as normal user.")
        modules.auth.run_as_root(" ".join(sys.argv[1:]))
        exit() 
    
    main()
else:
    print(f"{error} Directly importing ppm launcher is not recommend for managing system packages, you should be importing the modules of ppm, not the launcher.")
    print(f"{info} See more infomation at https://wiki.ppm.mom/importing-launcher")
