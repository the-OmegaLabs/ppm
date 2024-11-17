# Plusto Package Manager

A simple package manager written in Python, currently supporting the `dpkg` format. 

## Overview
Plusto Package Manager is a sleek, lightweight hybrid package manager for Linux. Now we are testing dpkg.

We are considering expanding support in future versions to include other repositories, such as Archlinux User Repo's like Plusto User Repo (pur), Debian's deb, Fedora’s rpm. This way, Plusto Package Manager will be able to better cater to the needs of various Linux users.

The legacy version of Plusto Package Manager (PPM) has several shortcomings, which is why we are in the process of rewriting a new version of PPM to address these issues and improve its functionality.
We are currently developing new version of ppm. You can try the old version in the `legacy/` directory.

## Requirements
- A Linux distribution with `dpkg` support.

## Installing

Use the following command to install required dependencies:

```bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/launcher.py /usr/bin/ppm
