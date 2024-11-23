### Plusto 包管理器

一个用 Python 编写的简单包管理器，目前支持 `dpkg` 格式。

## ⚠️ 如果您想使用最新版本的 Plusto 包管理器
请下载并使用 Plusto 包管理器的开发版本（即 `/new` 目录）。

## 概述
Plusto 包管理器是一个简洁、轻量的混合包管理器，适用于 Linux。目前我们正在测试 `dpkg`。

我们考虑在未来版本中扩展支持其他仓库，例如 ArchLinux 用户库（如 Plusto 用户库 `pur`）、Debian 的 `deb`、Fedora 的 `rpm`。这样，Plusto 包管理器将能够更好地满足各种 Linux 用户的需求。

旧版本的 Plusto 包管理器（PPM）存在一些不足，因此我们正在重写一个新的 PPM 版本，以解决这些问题并改进其功能。
我们目前正在开发新版本的 PPM。您可以尝试旧版本，位于 `legacy/` 目录中。

## 要求
- 支持 `dpkg` 的 Linux 发行版。
- （如果您使用的是 Plusto 包管理器的开发版本，请安装 Python3 和 pip，因为我懒得做脚本 XD）

## 安装

使用以下命令安装所需依赖项：

```bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/launcher.py /usr/bin/ppm 
```


开发版：
```bash
sudo apt update && sudo apt install -y python3-minimal python3-requests python3-colorama python3-halo
sudo git clone https://github.com/Stevesuk0/ppm.git /opt/ppm
sudo ln /opt/ppm/new/ppm.py /usr/bin/ppm
（我还没有在任何 Linux 发行版上测试过，所以请向我报告任何错误，枪枪爆头好运连连🤗）
```
