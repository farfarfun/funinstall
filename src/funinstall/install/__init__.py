"""install 包，提供各类开发工具的安装器类和 CLI 命令注册。

支持的工具:
    - Homebrew (macOS)
    - code-server
    - frpc
    - Go
    - MCP Hub
    - new-api
    - Node.js
    - OneHub
    - ossutil
    - UIF
    - v2rayA
"""

from .command import app as install_app
from .brew import BrewInstall
from .code_server import CodeServerInstall
from .frpc import FrpcInstall
from .go import GoInstall
from .mcphub import FunMcpHub
from .newapi import NewApiInstall
from .nodejs import NodeJSInstall
from .onehub import FunOneHub
from .ossutil import OSSUtilInstall
from .uif import UIFInstall
from .v2rayA import V2RayAInstall

__all__ = [
    "install_app",
    "BrewInstall",
    "CodeServerInstall",
    "FrpcInstall",
    "FunMcpHub",
    "FunOneHub",
    "GoInstall",
    "NewApiInstall",
    "NodeJSInstall",
    "OSSUtilInstall",
    "UIFInstall",
    "V2RayAInstall",
]
