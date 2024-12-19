config_dir = ''
cache_dir = ''

import json
import os
import base64

def cleanCacheFolder():
    try:
        os.chdir(cache_dir)
        filelist = os.listdir()
        for i in filelist:
            os.remove(i)
        return (True, len(filelist))
    except:
        return (False, 0)

def getRepofromConfiguation(): 
    with open(f"{config_dir}/repo.json") as f:
        return json.loads(f.read())

def getRepofromCache():
    config_repolist = getRepofromConfiguation()

    cachelist = {
        base64.b64decode(i.split('.ppmlist')[0]).decode()
        for i in os.listdir(cache_dir) if '.ppmlist' in i
    }
    repolist = [repo for repo in config_repolist if repo['name'] in cachelist]

    return repolist


    
    

def initRepoConfig():
    example_repo = [
        {
            'name': 'System Base',
            'type': 'dpkg',
            'url': 'http://mirrors.sdu.edu.cn/debian',
            'codename': 'testing',
            'category': 'main/binary-amd64',
        },
        {
            'name': 'Plusto User Repo',
            'type': 'pur',
            'url':  'http://ppm.stevesuk.eu.org/omegaos',
            'codename': 'sunset',
        },
    ]

    with open(config_dir + '/repo.json', 'w') as f:
        f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))
    
    return True