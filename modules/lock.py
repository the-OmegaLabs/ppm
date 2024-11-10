import os

def lock_disable():
    try:
        os.remove('/var/cache/ppm/ppm.lck')
        return True
    except:
        return False

def lock_enable():
    with open('/var/cache/ppm/ppm.lck', 'w') as f:
        f.write('')

def lock_check():
    return os.path.exists('/var/cache/ppm/ppm.lck')