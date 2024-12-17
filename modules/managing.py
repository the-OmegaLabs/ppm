# Package managing module 

import json
import requests
import os
import base64
import lzma

cache_dir = ''
config_dir = ''

def cleanCacheFolder():
    try:
        os.chdir(cache_dir)
        filelist = os.listdir()
        for i in filelist:
            os.remove(i)
        return (True, len(filelist))
    except:
        return (False, 0)

def dpkg_getInstalled(): # return     
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

def updateMetadata(repo: dict):
    """
    for repo in repos:
        if repo['type'] == 'deb':
            print(f"{info} Updating package list: {repo['name']} ({repo['type']})...")
            print(f"{info} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages", end='\r')
            url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
            try:
                response = requests.get(url)
                print(f"{get} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
            except:
                print(f"{error} {repo['url'].split('//')[-1].split('/')[0]} {repo['codename']} {repo['category']} Packages")
            path = f"{cache_dir}/{repo['name'].lower().replace(' ', '_')}"
            with open(f'{path}.xz', 'wb') as f:
                f.write(response.content)

            print(f"{info} Converting apt package list \"{repo['name']}\" to ppm format.")


            with lzma.open(f'{path}.xz') as compressed:
                with open(f'{path}.raw', 'wb') as uncompressed:
                    uncompressed.write(compressed.read())

            package_list = parse_packages(f'{path}.raw')
            save_packages_to_json(package_list, path)
            print(f"{success} Successfully updated {repo['name']} ({repo['type']}).")
            
        else:
            print(f"{warn} Unable to parse package source {repo['name']} ({repo['type']}), ignoring this item.")

    print(f'{success} All package list files have been updated.')"""

    if repo['type'] == 'dpkg':
        url = f"{repo['url']}/dists/{repo['codename']}/{repo['category']}/Packages.xz"
        try:
            response = requests.get(url)
        except:
            return (False, response)
        path = f"{cache_dir}/{base64.b64encode(repo['name'].encode('utf-8')).decode()}"
        with open(f'{path}.xz', 'wb') as f:
            f.write(response.content)
                
        with lzma.open(f'{path}.xz') as compressed:
            data = compressed.read().decode()
        
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

        with open(f'{path}.json', 'w') as f:
            f.write(json.dumps(packages_dicts, ensure_ascii=False, indent=4))