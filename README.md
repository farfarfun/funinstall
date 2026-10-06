# funinstall

[![PyPI Version](https://img.shields.io/pypi/v/funinstall.svg)](https://pypi.org/project/funinstall/)
[![License](https://img.shields.io/pypi/l/funinstall.svg)](https://github.com/farfarfun/funinstall/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/funinstall.svg)](https://pypi.org/project/funinstall/)

funinstall 是一个简单易用的工具包，用于一键安装各种开发工具和环境。

## 安装

```bash
uv tool install funinstall
```

## 功能特点

- 🚀 **简单易用**: 基于 Typer 构建的直观命令行界面
- 🔧 **多平台支持**: 支持 macOS、Linux、Windows 三大操作系统
- 📦 **丰富工具**: 涵盖开发环境、开发工具、网络工具、API管理等多个类别
- ⚡ **智能安装**: 自动检测系统架构和已安装软件，避免重复安装
- 🎯 **版本控制**: 支持指定版本安装和版本更新
- 🛡️ **安全可靠**: 从官方源下载，确保软件安全性

## 支持的安装工具

| 类别 | 工具名称 | 安装命令 | 说明 | macOS | Linux | Windows |
|------|----------|----------|------|-------|-------|---------|
| **开发环境** | Go 语言 | `funinstall install go` | Go 语言开发环境 | ✅ | ✅ | ✅ |
| | NodeJS | `funinstall install nodejs` | NodeJS 开发环境 | ✅ | ✅ | ✅ |
| | Homebrew | `funinstall install brew` | macOS 包管理器 | ✅ | ❌ | ❌ |
| **开发工具** | Code Server | `funinstall install code-server` | 基于 Web 的 VS Code 服务器 | ❌ | ✅ | ❌ |
| | OSS工具 | `funinstall install ossutil` | 阿里云对象存储命令行工具 | ✅ | ✅ | ✅ |
| **网络工具** | V2rayA | `funinstall install v2raya` | 网络代理工具 | ✅ | ✅ | ❌ |
| | FRP客户端 | `funinstall install frpc` | 内网穿透工具 | ❌ | ✅ | ❌ |
| **API管理** | New API | `funinstall install new-api` | 接口管理工具 | ✅ | ✅ | ✅ |
| | OneHub | `funinstall install onehub` | API 网关工具 | ✅ | ✅ | ✅ |
| **其他工具** | UIF | `funinstall install uif` | 通用工具 | ❌ | ✅ | ❌ |

### 使用示例

```bash
# 安装 Go 语言环境
funinstall install go

# 安装指定版本的 NodeJS
funinstall install nodejs --version 18.17.0

# 安装最新版本的 NodeJS
funinstall install nodejs --latest

# 安装阿里云 OSS 工具
funinstall install ossutil

# 查看所有可用命令
funinstall --help
funinstall install --help
```

## 开发

### 依赖项

- Python >= 3.12
- funserver >= 1.0.59
- funshell >= 1.0.5
- farlog >= 1.1.7
- requests >= 2.31.0

### 贡献

欢迎提交 issues 和 pull requests 到 [GitHub 仓库](https://github.com/farfarfun/funinstall)。

## 许可证

本项目基于 [MIT](LICENSE) 协议开源。

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
