# Package managing module 

import json
import requests
import os
import base64
import lzma
import io

cache_dir = ''
config_dir = ''

def dpkg_getInstalled(): # return package with version
    with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f: # retrieving dpkg information using dpkg-query
        a = f.read().strip().split(',')
        installed = {}
        
        for i in a:
            parts = i.split('/')
            if len(parts) == 2 and parts[1]: 
                installed[parts[0]] = parts[1]
        
        return installed
    
def dpkg_refreshInstalled(): # It will return how many dpkg package you installed.
    installed = dpkg_getInstalled()
    with open(cache_dir + '/installed_dpkg.json', 'w') as f:
        f.write(json.dumps(installed, ensure_ascii=False, indent=4))
    return len(installed)

def searchPackage(packname: str, repo: dict):
    repo_filepath = f"{cache_dir}/{base64.b64encode(repo['name'].encode()).decode()}.ppmlist"

    with open(repo_filepath) as f:
        packages = json.loads(f.read())

    return packages.get(packname, None)

def updateMetadata(repo: dict):
    if repo['type'] == 'dpkg':
        url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
        try:
            response = requests.get(url)
        except Exception as f:
            return False, f, response
        
        path = f"{cache_dir}/{base64.b64encode(repo['name'].encode('utf-8')).decode()}"
        
        try:
            with lzma.open(io.BytesIO(response.content)) as compressed:  
                data = compressed.read().decode('utf-8')
        except Exception as f:
            return False, f, response

        packages = data.strip().split('\n\n')
        packages_dicts = {}

        for pkg_info in packages:
            package_dict = {}
            for line in pkg_info.strip().split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    package_dict[key] = value.strip()
            
            package_name = package_dict.get("Package", "unknown_package")
            packages_dicts[package_name] = package_dict

        with open(f'{path}.ppmlist', 'w') as f:
            f.write(json.dumps(packages_dicts, ensure_ascii=False, indent=4))
        return True, None, response
    else:
        return False, None, None