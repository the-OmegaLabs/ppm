# command interface intry

import sys
import os
import colorama

###########################################

module_path = os.getcwd() # ppm core path

sys.path.append(module_path)

###########################################

import ppm.Core as core
import ppm.Style 

style = ppm.Style.get_style()

success = style.success
infomation = style.infomation
warning = style.warning
error = style.error

manager = core.Manager()
manager.root_path = './data'

if not manager.init():
    print(f'{error} Error when initializing ppm.')

if len(sys.argv) < 2:  # Direct execution
    print(f'{error} Please provide complete arguments.')
    print()
    print(f'{infomation} ppm version {manager.version}')
    print('Usage: ppm [options] command [packages]')
    print()
    print('Plusto Package Manager (ppm) is a hybrid package manager for Omega Linux.')
    print('You are currently using the command-line frontend of Plusto Package Manager,')
    print('which provides functionality to search, manage, and retrieve package information.')
    print()
    print(f'Loaded {len(manager.commands)} commands:')
    for module in manager.commands:
        print(f'  {module} - {manager.commands.get(module).module_desc}')

    print()
    print('This program is currently in early Alpha. If you encounter any issues or bugs,')
    print('please report them at [https://github.com/the-OmegaLabs/ppm/issues].')
