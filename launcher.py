#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import json

init(autoreset=False) # init colorama
sys.setrecursionlimit(1500) 

# Define different message types with colored formatting
info_character = '##'
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

version = "0.2"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = '/opt/ppm/localization'

with open(f'{locale_dir}/zh_CN.json') as f:
    localization = json.loads(f.read())

sys.path.append(launcher_dir) # Add custom path for ppm modules
import modules
import modules.auth
import modules.managing
import modules.config
import modules.lock

modules.lock.cache_dir = cache_dir
modules.managing.cache_dir = cache_dir
modules.managing.config_dir = config_dir
modules.config.cache_dir = cache_dir
modules.config.config_dir = config_dir

print(f'ppm {version}')


def main():
    if len(sys.argv) < 2:
        print(f"{error} {localization['no_enough_arguments']}")
        print(localization['help_text'])
        exit()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'init':
        if modules.config.initRepoConfig():
            print(f'{success} {localization["configuration_initialized"]}')
    
    elif command == 'download':
        repolist = modules.config.getRepofromCache() 
        for repo in repolist:
            modules.managing.loadPackages(repo) # precaching
            for package_name in args:
                
                packinfo = modules.managing.downloadPackage(package_name, '.', repo)

    elif command == 'search':
        repolist = modules.config.getRepofromCache() 
        for repo in repolist:
            modules.managing.loadPackages(repo) # precaching
            for package_name in args:
                packinfo = modules.managing.searchPackage(package_name)
                if packinfo:
                    homepage = ''
                    if not packinfo.get('Homepage', None) is None:
                        homepage = f"\n      {localization['see_website']}: {packinfo['Homepage']}"
                    print(f"{success} {repo['name']}: {packinfo['Package']}, {localization['version']} {packinfo['Version']}\n   by {packinfo['Maintainer']}\n      {packinfo['Description']}{homepage}")
                else:
                    print(f"{error} {localization['package']} \"{package_name}\" {localization['not_found']}")

    elif command == 'clean':
        cleaning = modules.config.cleanCacheFolder()
        if cleaning[0]: # bool
            if cleaning[1] == 0:
                print(f"{info} {localization['nothing_clean']}") 
            else:
                print(f"{success} {localization['success_clean']} {cleaning[1]} {localization['cache_files']}")
        else:
            print(f"{error} {localization['failed_clean']}")

    elif command == 'refresh':
        print(f"{info} {localization['refreshing']}...")
        installed = modules.managing.dpkg_refreshInstalled()
        print(f"{info} {localization['current_system']} {installed} {localization['installed_dpkg']}")

    elif command == 'help':
        print(localization["help_text"])

    elif command == 'update':
        repos = modules.config.getRepofromConfiguation()
        print(f"{info} {localization['found']} {len(repos)} {localization['repo_from_config']}...")
        for repo in repos:
            print(f"{info} {localization['update_package_list']}: {repo['name']} ({repo['type']})...", end='')
            sys.stdout.flush()
            if modules.managing.updateMetadata(repo)[0]:
                print(f"\r{success} {localization['updated_package_list']}: {repo['name']} ({repo['type']})...")
            else:
                print(f"\r{warn} {localization['cant_process_package_list']} \"{repo['name']} ({repo['type']})\", {localization['ignore_item']}")

    elif command == 'reset':
        if modules.lock.disable():
            print(f"{success} {localization['success_remove_lock']}")
        else:
            print(f"{error} {localization['failed_remove_lock']}")
        
    else:
        print(f"{error} {localization['provided_command_not_found']}")

if __name__ == "__main__":
    if modules.auth.checkIsRoot() is False:
        print(f'{warn} {localization["running_as_normal_user"]}')
        modules.auth.run_as_root(" ".join(sys.argv[1:]))
        exit() 

    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(launcher_dir, exist_ok=True)
    os.makedirs(locale_dir, exist_ok=True)
    
    main()
else:
    print(f"{error} {localization['importing_launcher']}")
    print(f"{info} {localization['see_website']} https://wiki.ppm.mom/importing-launcher")
