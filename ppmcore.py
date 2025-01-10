import sys
import os
import subprocess
import base64
import lzma
import io
import json
import requests

##############################################
# Directory settings:
# Running another function before set these variable.
cache_dir = ''
config_dir = ''
dependency_cache = {}
all_packages_cache = {}

##############################################
# Misc functions:
def isColorSupported():
    if not sys.stdout.isatty():
        return False
    term = os.getenv('TERM', '').lower()
    colorterm = os.getenv('COLORTERM', '').lower()

    if "color" in term or "256color" in term or "truecolor" in colorterm:
        return True
    try:
        colors = int(subprocess.check_output(['tput', 'colors']))
        if colors > 0:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def runAsRoot(args):
    subprocess.run(['sudo', 'sh', '-c', f"cd {os.getcwd()}; /bin/python3 launcher.py {args}"], check=True)

def checkIsRoot():  # return true when user is root
    return os.getuid() == 0

def hello():
    print('Hello, World!')

##############################################
# lock functions:
def lockDisable():
    try:
        os.remove(cache_dir + '/ppm.lck')
        return True
    except:
        return False


def lockEnable():
    with open(cache_dir + '/ppm.lck', 'w') as f:
        f.write('')


def lockCheck():
    return os.path.exists(cache_dir + '/ppm.lck')

##############################################
# Cleaning functions:
def cleanTempFolder():
    os.chdir(f'{cache_dir}/temp')
    filelist = os.listdir()
    count = 0
    for i in filelist:
        try:
            os.remove(i)
            count += 1
        except:
            pass
    return len(filelist)

def cleanCacheFolder():
    os.chdir(cache_dir)
    filelist = os.listdir()
    count = 0
    for i in filelist:
        try:
            os.remove(i)
            count += 1
        except:
            pass

    count += cleanTempFolder()
    
    return (True, count)

##############################################
# dpkg management functions:
def dpkg_getInstalled():  # return package with version
    # retrieving dpkg information using dpkg-query
    with os.popen("dpkg-query -W -f='${Package}/${Version},'") as f:
        a = f.read().strip().split(',')
        installed = {}

        for i in a:
            parts = i.split('/')
            if len(parts) == 2 and parts[1]:
                installed[parts[0]] = parts[1]

        return installed


def dpkg_refreshInstalled():  # It will return how many dpkg package you installed.
    installed = dpkg_getInstalled()
    with open(cache_dir + '/installed_dpkg.json', 'w') as f:
        f.write(json.dumps(installed, ensure_ascii=False, indent=4))
    return len(installed)


def dpkg_loadPackages(repo: dict):
    global all_packages_cache
    all_packages_cache = {}
    repo_filepath = f"{cache_dir}/{base64.b64encode(repo['name'].encode()).decode()}.ppmlist"

    with open(repo_filepath) as f:
        packages = json.loads(f.read())

    all_packages_cache = packages


def dpkg_searchPackage(packname: str):
    return dict(all_packages_cache).get(packname, None)


def dpkg_extractPackageNames(depends_str: str):
    package_names = depends_str.split(",")

    cleaned_package_names = set()
    for package in package_names:
        parts = package.strip().split()

        if parts:
            cleaned_package_names.add(parts[0])

    return cleaned_package_names


def dpkg_getDependencies(packname: str, visited=None):
    if visited is None:
        visited = set()

    if packname in visited:
        return set()

    visited.add(packname)

    package_info = dpkg_searchPackage(packname)
    if not package_info:
        return set()

    depends_str = package_info.get("Depends", "")
    if not depends_str:
        return set()

    dependencies = dpkg_extractPackageNames(depends_str)

    all_dependencies = set(dependencies)

    for dep in dependencies:
        all_dependencies.update(dpkg_getDependencies(dep, visited))

    return list(all_dependencies)


def dpkg_downloadPackage(packname: str, path: str, repo: dict):
    os.makedirs(path, exist_ok=True)
    oldPath = os.getcwd()
    os.chdir(path)

    if isinstance(packname, set):
        packname = list(packname)[0]

    packageInfo = dpkg_searchPackage(packname)

    url = f"{repo['url']}/{packageInfo['Filename']}"
    response = requests.get(url)
    filename = url.split('/')[-1]

    with open(filename, 'wb') as f:
        f.write(response.content)

    os.chdir(oldPath)

    return filename


def dpkg_installPackage(packname: str):
    subprocess.run(['sudo', 'dpkg', '-i', packname], check=True)


def dpkg_installPackagesfromDir(path):
    oldPath = os.getcwd()
    os.chdir(path)
    subprocess.run(['sudo', 'dpkg', '-i', '*.deb'], check=True)
    os.chdir(oldPath)


def dpkg_updateMetadata(repo: dict):
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
##############################################
# configuration functions:
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
            'codename': 'bookworm',
            'category': 'main/binary-amd64',
        },
    ]

    with open(config_dir + '/repo.json', 'w') as f:
        f.write(json.dumps(example_repo, indent=4, ensure_ascii=False))

    return True

##############################################