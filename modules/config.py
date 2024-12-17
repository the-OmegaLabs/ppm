config_dir = ''

import json

def getRepofromConfiguation():
    with open(f"{config_dir}/repo.json") as f:
        return json.loads(f.read())