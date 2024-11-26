# Plusto 包管理器

## [English Documentation / 英文文档](readme.md)

Plusto 包管理器是一个 *轻量级、可扩展、易用且可混合* 的包管理器，使用 Python 编写。它对用户友好，高度可定制，且设计时考虑到了更方便的扩展性。目前，它支持 `dpkg` 和 `winget` 格式。

### ⚠️ Windows 用户注意
如果你是 Windows 用户，请使用 Plusto 包管理器的 winget 版本（此为概念版本）（位于 `/windows` 目录）。

## 概述

Plusto 包管理器是一个混合型包管理器，支持 Linux 系统的 `dpkg` 格式。目前正在进行测试，未来的版本计划合并多个 Linux 包格式，比如 Debian 的 `.deb`、Fedora 的 `.rpm` 等，这样 Plusto 包管理器将支持更多格式，提供更好的兼容性和灵活性，满足不同 Linux 用户的需求。

**遗留版本**的 ppm 存在一些不足之处，因此我们正在重写新版本来解决这些问题，并增强功能。你可以尝试旧版本，它们位于 `/legacy/` 目录。

你还可以尝试 **概念版本**，以体验最新的功能，位于 `/new/` 目录。注意：我们尚未在所有 Linux 发行版上进行测试，因此如果遇到任何问题，请反馈。

## 系统要求

- 支持 `dpkg` 格式的 Linux 发行版。
- 如果你使用的是 Plusto 包管理器的概念版本，请确保已安装 Python 3 和 pip（目前我们没有提供安装脚本，请耐心等待）。

## 安装

在我们的网站中查看：[快速开始](https://ppm.stevesuk.eu.org/getting-started.html)
