import json

config_dir = ''

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