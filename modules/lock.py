import os

cache_dir = ''

def lock_disable():
    try:
        os.remove(cache_dir + '/ppm.lck')
        return True
    except:
        return False

def lock_enable():
    with open(cache_dir + '/ppm.lck', 'w') as f:
        f.write('')

def lock_check():
    return os.path.exists(cache_dir + '/ppm.lck')