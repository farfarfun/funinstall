# API 文档

## 概述

funinstall 提供了一套统一的安装类接口，用于在不同平台上安装各种开发工具。所有安装类都继承自 `BaseInstall` 基类。

## 基础接口

### BaseInstall

所有安装类的基类，定义了统一的安装接口。

```python
from funserver.servers.base.install import BaseInstall

class BaseInstall:
    def install(self) -> bool:
        """根据当前系统自动选择安装方法"""
        
    def install_macos(self, *args, **kwargs) -> bool:
        """macOS 系统安装方法"""
        
    def install_linux(self, *args, **kwargs) -> bool:
        """Linux 系统安装方法"""
        
    def install_windows(self, *args, **kwargs) -> bool:
        """Windows 系统安装方法"""
```

## 安装类列表

### 开发环境

#### GoInstall

Go 语言开发环境安装类。

**类定义**
```python
class GoInstall(BaseInstall):
    def __init__(self, version: str = "", force=False, *args, **kwargs)
```

**参数说明**
- `version` (str): 指定安装的Go版本，默认为空（安装最新版本）
- `force` (bool): 是否强制重新安装，默认为False

**方法**
- `is_installed() -> bool`: 检查Go是否已安装
- `install_macos()`: 使用Homebrew安装Go
- `install_linux()`: 使用官方脚本安装Go
- `install_windows()`: 使用MSI安装包安装Go

**使用示例**
```python
from funinstall.install.go import GoInstall

# 安装最新版本
installer = GoInstall()
installer.install()

# 安装指定版本
installer = GoInstall(version="1.21.0")
installer.install()

# 强制重新安装
installer = GoInstall(force=True)
installer.install()
```

#### NodeJSInstall

NodeJS 开发环境安装类。

**类定义**
```python
class NodeJSInstall(BaseInstall):
    def __init__(self, version=None, lasted=False, update=False, force=False, *args, **kwargs)
```

**参数说明**
- `version` (str): 指定安装的NodeJS版本
- `lasted` (bool): 是否安装最新版本
- `update` (bool): 是否更新当前版本
- `force` (bool): 是否强制重新安装

**方法**
- `is_installed() -> bool`: 检查NodeJS是否已安装
- `install_macos()`: 使用Homebrew安装NodeJS
- `install_linux()`: 使用官方脚本安装NodeJS
- `install_windows()`: 使用MSI安装包安装NodeJS

**使用示例**
```python
from funinstall.install.nodejs import NodeJSInstall

# 安装默认版本
installer = NodeJSInstall()
installer.install()

# 安装指定版本
installer = NodeJSInstall(version="18.17.0")
installer.install()

# 安装最新版本
installer = NodeJSInstall(lasted=True)
installer.install()
```

### 开发工具

#### OSSUtilInstall

阿里云对象存储OSS命令行工具安装类。

**类定义**
```python
class OSSUtilInstall(BaseInstall):
    def __init__(self, version="2.1.2", force=False, *args, **kwargs)
```

**参数说明**
- `version` (str): 指定安装的ossutil版本，默认为"2.1.2"
- `force` (bool): 是否强制重新安装，默认为False

**特性**
- 支持多平台：macOS、Linux、Windows
- 自动架构检测：x86_64、ARM64、x86等
- 智能安装检查：避免重复安装
- 统一安装路径：`~/opt/bin/`

**方法**
- `is_installed() -> bool`: 检查ossutil是否已安装
- `install_macos()`: 在macOS上安装ossutil
- `install_linux()`: 在Linux上安装ossutil  
- `install_windows()`: 在Windows上安装ossutil

**使用示例**
```python
from funinstall.install.ossutil import OSSUtilInstall

# 安装默认版本
installer = OSSUtilInstall()
installer.install()

# 安装指定版本
installer = OSSUtilInstall(version="2.1.2")
installer.install()

# 强制重新安装
installer = OSSUtilInstall(force=True)
installer.install()
```

#### CodeServerInstall

VS Code Server 安装类。

**类定义**
```python
class CodeServerInstall(BaseInstall):
    def __init__(self, *args, **kwargs)
```

**使用示例**
```python
from funinstall.install.code_server import CodeServerInstall

installer = CodeServerInstall()
installer.install()
```

### 网络工具

#### V2RayAInstall

V2rayA 网络代理工具安装类。

**类定义**
```python
class V2RayAInstall(BaseInstall):
    def __init__(self, version=None, lasted=False, update=False, *args, **kwargs)
```

#### FrpcInstall

FRP客户端安装类。

**类定义**
```python
class FrpcInstall(BaseInstall):
    def __init__(self, *args, **kwargs)
```

### API管理工具

#### NewApiInstall

New API 接口管理工具安装类。

**类定义**
```python
class NewApiInstall(BaseInstall):
    def __init__(self, overwrite=False, *args, **kwargs)
```

#### FunOneHub

OneHub API 网关工具安装类。

**类定义**
```python
class FunOneHub(BaseServer):
    def __init__(self, overwrite: bool = False, *args, **kwargs)
```

## 通用模式

### 安装前检查

所有现代化的安装类都实现了 `is_installed()` 方法：

```python
def is_installed(self) -> bool:
    """
    检查工具是否已安装
    返回True表示已安装，False表示未安装
    """
```

### 错误处理

所有安装方法都应该包含适当的错误处理：

```python
def install_platform(self, *args, **kwargs) -> bool:
    try:
        # 安装逻辑
        return True
    except Exception as e:
        logger.error(f"安装失败: {e}")
        return False
```

### 日志记录

使用统一的日志记录格式：

```python
from funutil import getLogger

logger = getLogger("funinstall")

# 信息日志
logger.info("开始安装...")

# 成功日志
logger.success("安装成功")

# 错误日志
logger.error("安装失败")

# 警告日志
logger.warning("检测到潜在问题")
```

## 扩展指南

### 创建新的安装类

1. 继承 `BaseInstall` 基类
2. 实现必要的安装方法
3. 添加安装前检查逻辑
4. 实现错误处理和日志记录
5. 在 `command.py` 中注册命令

```python
import os
import platform

from funbuild.shell import run_shell
from funserver.servers.base.install import BaseInstall
from funutil import getLogger

logger = getLogger("funinstall")

class NewToolInstall(BaseInstall):
    def __init__(self, version=None, force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.force = force

    def is_installed(self) -> bool:
        """检查工具是否已安装"""
        try:
            run_shell("newtool --version")
            logger.info("检测到系统中已安装 NewTool")
            return True
        except:
            return False

    def install_macos(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info("NewTool 已安装，跳过安装")
            return True
        
        # macOS 安装逻辑
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info("NewTool 已安装，跳过安装")
            return True
        
        # Linux 安装逻辑
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info("NewTool 已安装，跳过安装")
            return True
        
        # Windows 安装逻辑
        return True
```
