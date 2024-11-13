# Plusto Package Manager

A simple package manager written in Python, currently supporting the `dpkg` format. 

## Overview
Plusto Package Manager is designed to be a straightforward tool for managing packages. While it currently supports Debian packages (`dpkg` format), we are considering adding support for other formats, such as Arch Linux’s AUR in future versions.

We are currently refactoring the code. You can use the old version in the `leagcy/` directory.

## Requirements
- A Linux distribution with `dpkg` support.

## Installing

Use the following command to install required dependencies:

```bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/launcher.py /usr/bin/ppm
