import os
# import dbus


def run_as_root(args):
    os.system(f"sudo sh -c 'cd {os.getcwd()}; /bin/python3 {args}'") 

def check_is_root(): # return true when user is root
    return os.getuid() == 0 
