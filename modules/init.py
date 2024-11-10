import json
import os

def init_config():
    os.makedirs('/etc/ppm', exist_ok=True)
    os.chdir('/etc/ppm')

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

    with open('repo.json', 'w') as f:
        f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))
    
    return True