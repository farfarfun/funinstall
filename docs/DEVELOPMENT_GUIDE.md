# 开发指南

## 项目概述

funinstall 是一个用于快速安装各种开发工具和环境的Python包。项目采用模块化设计，支持多平台安装，具有统一的接口和良好的扩展性。

## 开发环境搭建

### 系统要求

- Python >= 3.9
- Git
- 支持的操作系统：macOS、Linux、Windows

### 环境配置

1. **克隆项目**
   ```bash
   git clone https://github.com/farfarfun/funinstall.git
   cd funinstall
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # 或
   .venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # 如果存在开发依赖
   ```

## 项目结构

```
funinstall/
├── src/
│   └── funinstall/
│       ├── __init__.py
│       ├── command.py              # 主命令入口
│       ├── common/                 # 公共模块
│       └── install/                # 安装模块
│           ├── __init__.py
│           ├── command.py          # 安装命令定义
│           ├── brew.py             # Homebrew安装
│           ├── code_server.py      # Code Server安装
│           ├── frpc.py             # FRP客户端安装
│           ├── go.py               # Go语言安装
│           ├── newapi.py           # New API安装
│           ├── nodejs.py           # NodeJS安装
│           ├── oneapi.py           # One API安装
│           ├── onehub.py           # OneHub安装
│           ├── ossutil.py          # OSS工具安装
│           ├── uif.py              # UIF工具安装
│           └── v2rayA.py           # V2rayA安装
├── docs/                           # 文档目录
│   ├── API.md                      # API文档
│   ├── CHANGELOG.md                # 变更日志
│   └── DEVELOPMENT_GUIDE.md        # 开发指南
├── tests/                          # 测试目录
├── README.md                       # 项目说明
├── pyproject.toml                  # 项目配置
└── LICENSE                         # 许可证
```

## 开发规范

### 代码规范

1. **语言规范**
   - 注释使用中文
   - 对话和日志使用中文
   - 遵循PEP8编码规范

2. **文档字符串**
   ```python
   def install_macos(self, *args, **kwargs) -> bool:
       """
       在macOS系统上安装工具
       
       Args:
           *args: 位置参数
           **kwargs: 关键字参数
           
       Returns:
           bool: 安装成功返回True，失败返回False
       """
   ```

3. **日志记录**
   ```python
   from funutil import getLogger
   
   logger = getLogger("funinstall")
   
   logger.info("开始安装...")
   logger.success("安装成功")
   logger.error("安装失败")
   logger.warning("检测到潜在问题")
   ```

### 安装类开发规范

#### 1. 基础结构

所有安装类必须继承 `BaseInstall` 并实现以下结构：

```python
import os
import platform

from funbuild.shell import run_shell
from funserver.servers.base.install import BaseInstall
from funutil import getLogger

logger = getLogger("funinstall")

class ToolInstall(BaseInstall):
    def __init__(self, version=None, force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.force = force

    def is_installed(self) -> bool:
        """检查工具是否已安装"""
        # 实现检查逻辑
        pass

    def install_macos(self, *args, **kwargs) -> bool:
        """macOS安装方法"""
        # 安装前检查
        if not self.force and self.is_installed():
            logger.info("工具已安装，跳过安装")
            return True
        
        # 实现安装逻辑
        pass

    def install_linux(self, *args, **kwargs) -> bool:
        """Linux安装方法"""
        # 安装前检查
        if not self.force and self.is_installed():
            logger.info("工具已安装，跳过安装")
            return True
        
        # 实现安装逻辑
        pass

    def install_windows(self, *args, **kwargs) -> bool:
        """Windows安装方法"""
        # 安装前检查
        if not self.force and self.is_installed():
            logger.info("工具已安装，跳过安装")
            return True
        
        # 实现安装逻辑
        pass
```

#### 2. 必需实现的方法

- `is_installed()`: 检查工具是否已安装
- `install_macos()`: macOS平台安装方法
- `install_linux()`: Linux平台安装方法
- `install_windows()`: Windows平台安装方法

#### 3. 安装前检查

每个安装方法都必须在开始时检查是否已安装：

```python
def install_platform(self, *args, **kwargs) -> bool:
    # 检查是否已安装
    if not self.force and self.is_installed():
        logger.info("工具已安装，跳过安装。如需重新安装，请使用 force=True 参数")
        return True
    
    # 安装逻辑
    try:
        # 具体安装步骤
        logger.success("安装成功")
        return True
    except Exception as e:
        logger.error(f"安装失败: {e}")
        return False
```

#### 4. 错误处理

所有安装方法都应该包含完善的错误处理：

```python
def install_platform(self, *args, **kwargs) -> bool:
    try:
        # 安装逻辑
        return True
    except Exception as e:
        logger.error(f"安装失败: {e}")
        logger.info("安装失败，请手动下载安装")
        logger.info("下载地址: https://example.com/download")
        return False
```

### 命令注册

在 `install/command.py` 中注册新的安装命令：

```python
from .newtool import NewToolInstall

@app.command(name="newtool")
def install_newtool(
    version: str = typer.Option(None, "--version", "-v", help="工具版本"),
    force: bool = typer.Option(False, "--force", "-f", help="强制重新安装"),
) -> bool:
    return NewToolInstall(version=version, force=force).install()
```

在 `install/__init__.py` 中导出安装函数：

```python
from .command import install_newtool

__all__ = [
    # ... 其他导出
    "install_newtool",
]
```

## 测试要求

### 单元测试

- 测试覆盖率不低于80%
- 为每个安装类编写测试
- 模拟安装过程，避免实际安装

```python
import unittest
from unittest.mock import patch, MagicMock

class TestGoInstall(unittest.TestCase):
    def setUp(self):
        self.installer = GoInstall()
    
    @patch('funinstall.install.go.run_shell')
    def test_is_installed_true(self, mock_run_shell):
        mock_run_shell.return_value = "go version go1.21.0"
        self.assertTrue(self.installer.is_installed())
    
    @patch('funinstall.install.go.run_shell')
    def test_is_installed_false(self, mock_run_shell):
        mock_run_shell.side_effect = Exception("command not found")
        self.assertFalse(self.installer.is_installed())
```

### 集成测试

- 测试完整的安装流程
- 验证多平台兼容性
- 测试错误处理机制

## 版本管理

### 语义化版本

项目使用语义化版本号 (Semantic Versioning)：

- `MAJOR.MINOR.PATCH`
- MAJOR: 不兼容的API变更
- MINOR: 向后兼容的功能新增
- PATCH: 向后兼容的问题修复

### 发布流程

1. **更新版本号**
   ```bash
   # 在 pyproject.toml 中更新版本号
   version = "1.0.55"
   ```

2. **更新变更日志**
   ```bash
   # 在 docs/CHANGELOG.md 中记录变更
   ```

3. **创建Git标签**
   ```bash
   git tag v1.0.55
   git push origin v1.0.55
   ```

4. **发布到PyPI**
   ```bash
   python -m build
   python -m twine upload dist/*
   ```

## 贡献指南

### 提交规范

使用约定式提交 (Conventional Commits)：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(install): 添加Python安装支持

- 支持多版本Python安装
- 自动检测系统架构
- 添加Windows平台支持

Closes #123
```

### Pull Request流程

1. Fork项目
2. 创建功能分支
3. 实现功能并编写测试
4. 更新文档
5. 提交Pull Request
6. 代码审查
7. 合并到主分支

### 代码审查要点

- 代码符合项目规范
- 包含适当的测试
- 文档更新完整
- 无明显的性能问题
- 错误处理完善

## 常见问题

### Q: 如何添加新的安装工具？

A: 参考现有的安装类（如 `ossutil.py`），创建新的安装类，实现必需的方法，并在命令文件中注册。

### Q: 如何处理平台特定的安装逻辑？

A: 在对应的平台方法中实现特定逻辑，使用 `platform.machine()` 检测架构，使用适当的包管理器或安装方式。

### Q: 如何测试安装功能？

A: 使用mock模拟shell命令执行，避免实际安装。测试安装前检查、错误处理等逻辑。

### Q: 如何处理依赖冲突？

A: 在 `pyproject.toml` 中明确指定依赖版本范围，使用虚拟环境隔离开发环境。

## 联系方式

- GitHub Issues: https://github.com/farfarfun/funinstall/issues
- 邮箱: farfarfun@qq.com
- 组织: https://github.com/farfarfun
