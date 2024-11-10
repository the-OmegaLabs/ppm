import json
import os

def get_installed_status():
    with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f: # retrieving dpkg information using dpkg-query
        a = f.read().strip().split(',')
        installed = {}
        
        for i in a:
            parts = i.split('/')
            if len(parts) == 2 and parts[1]: 
                installed[parts[0]] = parts[1]
        
        return installed
    