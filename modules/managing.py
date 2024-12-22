# Package managing module 

import json
import requests
import os
import base64
import lzma
import io

cache_dir = ''
config_dir = ''
dependency_cache = {}
all_packages_cache = {}

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


def loadPackages(repo: dict):
    global all_packages_cache
    all_packages_cache = {}
    repo_filepath = f"{cache_dir}/{base64.b64encode(repo['name'].encode()).decode()}.ppmlist"
    
    with open(repo_filepath) as f:
        packages = json.loads(f.read())
    
    all_packages_cache = packages

def searchPackage(packname: str):
    return dict(all_packages_cache.get(packname, None))

def extractPackageNames(depends_str: str):
    package_names = depends_str.split(",")
    
    cleaned_package_names = set()  
    for package in package_names:
        parts = package.strip().split()
        
        if parts:
            cleaned_package_names.add(parts[0])  
    
    return cleaned_package_names

def getDependencies(packname: str, visited=None):
    if visited is None:
        visited = set()

    if packname in visited:
        return set()

    visited.add(packname)

    package_info = searchPackage(packname)
    if not package_info:
        return set()

    depends_str = package_info.get("Depends", "")
    if not depends_str:
        return set()

    dependencies = extractPackageNames(depends_str)

    all_dependencies = set(dependencies)

    for dep in dependencies:
        all_dependencies.update(getDependencies(dep, visited))

    return list(all_dependencies)

def downloadPackage(packname: str, path: str, repo: dict):
    oldPath = os.getcwd()
    os.chdir(path)

    packageInfo = searchPackage(list(packname)[0])

    url = f"{repo['url']}/{packageInfo['Filename']}"
    response = requests.get(url)
    filename = url.split('/')[-1]

    with open(filename, 'wb') as f:
        f.write(response.content)
        

    os.chdir(oldPath)
    

def updateMetadata(repo: dict):
    if repo['type'] == 'dpkg':
        url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
        try:
            response = requests.get(url)
        except Exception as f:
            return False, f
        
        path = f"{cache_dir}/{base64.b64encode(repo['name'].encode('utf-8')).decode()}"
        
        try:
            with lzma.open(io.BytesIO(response.content)) as compressed:  
                data = compressed.read().decode('utf-8')
        except Exception as f:
            return False, f

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