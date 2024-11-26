import os

def check_is_root():
    return os.getuid() == 0 