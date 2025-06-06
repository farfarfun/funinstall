# funinstall

[![PyPI Version](https://img.shields.io/pypi/v/funinstall.svg)](https://pypi.org/project/funinstall/)
[![License](https://img.shields.io/pypi/l/funinstall.svg)](https://github.com/farfarfun/funinstall/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/funinstall.svg)](https://pypi.org/project/funinstall/)

funinstall 是一个简单易用的工具包，用于一键安装各种开发工具和环境。

## 安装

```bash
pip install funinstall
```

## 功能特点

- 简单的命令行界面，基于 Typer 构建
- 支持多种开发工具的一键安装
- 灵活的版本选择和配置选项

## 支持的安装工具

### Go 语言

一键安装 Go 语言环境：

```bash
funinstall install go [--version VERSION]
```

### NodeJS

一键安装 NodeJS 环境：

```bash
funinstall install nodejs [--version VERSION] [--lasted] [--update]
```

选项说明：
- `--version/-v`: 指定安装的 NodeJS 版本
- `--lasted/-l`: 安装最新版本
- `--update/-u`: 更新当前版本

### Code Server

安装 Code Server：

```bash
funinstall install code-server
```

### 其他工具

查看所有可用的安装命令：

```bash
funinstall --help
```

## 开发

### 依赖项

- Python >= 3.9
- funbuild >= 1.6.3
- funsecret >= 1.4.56
- funutil >= 1.0.50

### 贡献

欢迎提交 issues 和 pull requests 到 [GitHub 仓库](https://github.com/farfarfun/funinstall)。

## 许可证

本项目采用 [LICENSE](LICENSE) 许可证。