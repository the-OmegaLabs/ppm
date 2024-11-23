# Plusto Package Manager
## [中国人点我](readme_chinese.md)

A simple package manager written in Python, currently supporting the `dpkg winget` format. 
## ⚠️If you is a windows user
Please download use the winget version of Plusto Package Manager (aka /windows directory).
## ⚠️If you want to use the latest version of Plusto Package Manager️
Please download use the dev version of Plusto Package Manager (aka /new directory).
## Overview
Plusto Package Manager is a sleek, lightweight hybrid package manager for Linux. Now we are testing dpkg.

We are considering expanding support in future versions to include other repositories, such as Archlinux User Repo's like Plusto User Repo (pur), Debian's deb, Fedora’s rpm. This way, Plusto Package Manager will be able to better cater to the needs of various Linux users.

The legacy version of Plusto Package Manager (PPM) has several shortcomings, which is why we are in the process of rewriting a new version of PPM to address these issues and improve its functionality.
We are currently developing new version of ppm. You can try the old version in the `legacy/` directory.

## Requirements
- A Linux distribution with `dpkg` support.
- (if you is using the dev version of Plusto Package Manager, plz install the python3 and pip, beacause i don't want to add the fucking install script XD)

## Installing

### On Linux
Use the following command to install required dependencies:
```
bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/launcher.py /usr/bin/ppm 
```
Dev ver:
```
bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/new/ppm.py /usr/bin/ppm
```
(i have not trying to make it work on any linux distro yet, so plz report any bugs to me, o7)
### On Windows
1. **Install Python**: Ensure you have Python installed. You can download it from the official website: https://www.python.org/downloads/
2. **Clone the Repository**:
   git clone https://github.com/Stevesuk0/ppm.git
3. **Create a Batch File**:
   - Open Notepad or any text editor.
   - Create a new file with the following content:
     @echo off
     python "C:\path\to\ppm\new\ppm.py" %*
   - Save the file as `ppm.bat` in a directory that is included in your system's PATH environment variable, such as `C:\Windows\System32`.
4. **Run PPM**:
   - Open Command Prompt and type `ppm` followed by any arguments you need.
