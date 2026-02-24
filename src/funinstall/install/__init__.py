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
