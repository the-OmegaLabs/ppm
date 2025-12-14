# command interface intry

import sys
import os
import time
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

lock = manager.hold_lock()

if not lock:
    print(f'{warning} Cannot acquire lock. Another instance may still be running.')

while not lock:
    if manager.hold_lock(): break
    
    print(f'{infomation} Waiting for another instance to finish...')
    
    time.sleep(1)

if not manager.init():
    print(f'{error} Error when initializing ppm.')
    sys.exit()

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

else:
    manager.execute(sys.argv[1], sys.argv[1:])