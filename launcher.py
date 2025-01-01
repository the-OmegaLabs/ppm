#!/usr/bin/python3

version = '0.4'

import sys
import os
import json
import utils.pConfig as config
import ppmcore

sys.setrecursionlimit(5000)

# Define different message types with colored formatting
if config.enable_color_output:
    success = config.success
    info = config.info
    warn = config.warn
    error = config.error
else:
    success = config.success_alt
    info = config.info_alt
    warn = config.warn_alt
    error = config.error_alt

def initDir():
    os.makedirs(config.cache_dir, exist_ok=True)
    os.makedirs(config.config_dir, exist_ok=True)
    os.makedirs(config.launcher_dir, exist_ok=True)
    os.makedirs(config.locale_dir, exist_ok=True)

with open(f'{config.locale_dir}/{config.language}.json') as f:
    localization = json.loads(f.read())

# sync modules config with pconfig
ppmcore.cache_dir = config.cache_dir
ppmcore.config_dir = config.config_dir

if config.print_version:
    print(f'ppm {version}')

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
clean        Clean ppm cache files
download     Download package by keyword (beta)"""

def main():
    if len(sys.argv) < 2:
        print(f"{error} {localization['no_enough_arguments']}")
        print(localization['help_text'])
        exit()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'init':
        if ppmcore.initRepoConfig():
            print(f'{success} {localization["configuration_initialized"]}')
    
    elif command == 'install':
        repolist = ppmcore.getRepofromCache() 
        willInstall = []
        for repo in repolist:
            ppmcore.dpkg_loadPackages(repo) # precaching
            for package_name in args:
                packageList = ppmcore.dpkg_getDependencies(package_name)
                packageList.append(package_name)
                print(f"{info} {localization['will_install']}", end='')
                for i in packageList:
                    print(i, end=' ')
                print()
                choice = input(f"{info} {localization['proceed']}? (Y/n) ")
                if choice == 'y' or not choice:
                    print(f"\n{info} {len(packageList)} packages will be installed.")
                    for i in range(len(packageList)):
                        print(f'\r{info} [{i + 1}/{len(packageList)}] Downloading package {packageList[i]}...           ', end='')
                        filename = ppmcore.dpkg_downloadPackage({packageList[i]}, f'{config.cache_dir}/temp', repo)
                        willInstall.append(filename)
                        print(f'\r{success} Downloaded package {packageList[i]}.')
                else:
                    return 1
        ppmcore.lockEnable()
        print(f"{info} {localization['select']} {len(packageList)} dpkg {localization['packages']}, {localization['call_dpkg']}")
        ppmcore.dpkg_installPackagesfromDir(f'{config.cache_dir}/temp')
        print(f"{success} Installed {len(packageList)} packages.")
        print(f"{info} Cleaning up temporary files...")
        oldPath = os.getcwd()
        ppmcore.cleanTempFolder()
        os.chdir(oldPath)
        print(f"{info} {localization['refreshing']}...")
        installed = ppmcore.dpkg_refreshInstalled()
        print(f"{info} {localization['current_system']} {installed} {localization['installed_dpkg']}")
        ppmcore.lockDisable()
        return 0


    elif command == 'download':
        if '--with-depends' in args:
            withDepend = True
            args.remove('--with-depends')
        else:
            withDepend = False

        repolist = ppmcore.getRepofromCache() 
        for repo in repolist:
            ppmcore.dpkg_loadPackages(repo) # precaching
            if withDepend:
                for package_name in args:
                    packageList = ppmcore.dpkg_getDependencies(package_name)
                    packageList.append(package_name)
                    print(f"{info} Will download these package: ", end='')
                    for i in packageList:
                        print(i, end=' ')
                    print(f"\n{info} {len(packageList)} packages will be download.")
                    for i in range(len(packageList)):
                        print(f'\r{info} [{i + 1}/{len(packageList)}] Downloading package {packageList[i]}...           ', end='')
                        packinfo = ppmcore.dpkg_downloadPackage({packageList[i]}, '.', repo)
                        print(f'\r{success} Downloaded package {packageList[i]}.')
            else:
                for package_name in args:
                    print(f'\r{info} Downloading package {package_name}...', end='')
                    packinfo = ppmcore.dpkg_downloadPackage(package_name, '.', repo)
                    print(f'\r{success} Downloaded package {package_name}.      ')

    elif command == 'search':
        repolist = ppmcore.getRepofromCache() 
        for repo in repolist:
            ppmcore.dpkg_loadPackages(repo) # precaching
            for package_name in args:
                packinfo = ppmcore.dpkg_searchPackage(package_name)
                if packinfo:
                    homepage = ''
                    if not packinfo.get('Homepage', None) is None:
                        homepage = f"\n      {localization['see_website']}: {packinfo['Homepage']}"
                    print(f"{success} {repo['name']}: {packinfo['Package']}, {localization['version']} {packinfo['Version']}\n   by {packinfo['Maintainer']}\n      {packinfo['Description']}{homepage}")
                else:
                    print(f"{error} {localization['package']} \"{package_name}\" {localization['not_found']}")

    elif command == 'clean':
        cleaning = ppmcore.cleanCacheFolder()
        if cleaning[0]: # bool
            if cleaning[1] == 0:
                print(f"{info} {localization['nothing_clean']}")
            else:
                print(f"{success} {localization['success_clean']} {cleaning[1]} {localization['cache_files']}")
        else:
            print(f"{error} {localization['failed_clean']}")

    elif command == 'refresh':
        print(f"{info} {localization['refreshing']}...")
        installed = ppmcore.dpkg_refreshInstalled()
        print(f"{info} {localization['current_system']} {installed} {localization['installed_dpkg']}")

    elif command == 'help':
        print(localization["help_text"])

    elif command == 'update':
        repos = ppmcore.getRepofromConfiguation()
        print(f"{info} {localization['found']} {len(repos)} {localization['repo_from_config']}...")
        for repo in repos:
            print(f"{info} {localization['update_package_list']}: {repo['name']} ({repo['type']})...", end='')
            sys.stdout.flush()
            if ppmcore.dpkg_updateMetadata(repo)[0]:
                print(f"\r{success} {localization['updated_package_list']}: {repo['name']} ({repo['type']})...")
            else:
                print(f"\r{warn} {localization['cant_process_package_list']} \"{repo['name']} ({repo['type']})\", {localization['ignore_item']}")

    elif command == 'reset':
        if ppmcore.lockDisable():
            print(f"{success} {localization['success_remove_lock']}")
        else:
            print(f"{error} {localization['failed_remove_lock']}")

    elif command == 'hello':
        ppmcore.hello()


    else:
        print(f"{error} {localization['provided_command_not_found']}")

    
if __name__ == "__main__":
    if not sys.stdin.isatty():
        print(f"{warn} {localization['running_in_pipe']}")
    if ppmcore.checkIsRoot() is False:
        print(f'{warn} {localization["running_as_normal_user"]}')
        ppmcore.runAsRoot(" ".join(sys.argv[1:]))
        exit() 
    initDir()
    main()
else:
    print(f"{error} {localization['importing_launcher']}")
    print(f"{info} {localization['see_website']} https://wiki.ppm.mom/importing-launcher")
