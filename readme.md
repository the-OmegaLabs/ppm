<img align="left" width="150" height="150" align="left" style="float: left; margin: 0 10px 0 0;" src="https://ppm.stevesuk.eu.org/icon.png"> <h1>Plusto Package Manager</h1>
<img align="left" src="https://img.shields.io/badge/Made%20with-Python-magenta?style=for-the-badge&logo=python&logoColor=magenta"><img src="https://img.shields.io/badge/Required-Linux-purple?style=for-the-badge&logo=linux&logoColor=purple"> *Simple, efficient, and compatible with multiple Linux package formats for software management.*

![Alt](https://repobeats.axiom.co/api/embed/28cf570b81bed278b472ceb028fbc9ffbb84715f.svg "Repobeats analytics image")

Plusto Package Manager is a *lightweight, easy-to-use, and mixable* package manager written in Python. It is user-friendly, highly customizable, and designed with easlier extensibility in mind. 

Format supports:
```
Debian Linux (Like):
  - apt       : √
  - dpkg      : × (wrapper in current version)
Red Hat Enterprise Linux (Like):
  - dnf / yum : ×
  - rpm       : ×
Arch Linux (like):
  - pacman    : ×
Alpine Linux:
  - apk       : ×
Plusto User Repo :
  - pur       : x
Windows Package Manager:
  - winget    : √ (experimental)
```
## Overview

Plusto Package Manager is a hybrid package manager for Linux, currently supporting the `dpkg` format. We are conducting tests, and future versions are planned to merge various Linux package formats, such as Debian's `.deb`, Fedora's `.rpm`, and others, so that Plusto Package Manager will support a broader range of formats, offering better compatibility and flexibility for different Linux users.

The **Legacy Version** of ppm had several shortcomings, which is why we are in the process of rewriting the new version to address these issues and enhance functionality. You can try the old version, they are in the `/legacy/` directory, Only can running on Debian-like Linux distro.

You can also try the **Concept Version** to enjoying the latest feature, they are in `/new/` directory. Note: We have not tested this on all Linux distributions yet, so please report any bugs or issues

## Installing

See [Getting Started](https://ppm.stevesuk.eu.org/getting-started.html) in our website.
