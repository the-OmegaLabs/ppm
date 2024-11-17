import json

config_dir = ''

def init_repo_config():
    example_repo = [
        {
            'name': 'OmegaOS Base',
            'type': 'deb',
            'url': 'http://mirrors.ustc.edu.cn/debian',
            'codename': 'testing',
            'category': 'main/binary-amd64',
        },
        {
            'name': 'OmegaOS Extra',
            'type': 'ppm',
            'url':  'http://ppm.stevesuk.eu.org/omegaos',
            'codename': 'sunset',
        },
    ]

    with open(config_dir + '/repo.json', 'w') as f:
        f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))
    
    return True