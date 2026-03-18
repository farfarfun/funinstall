"""install 子命令组，将各工具的安装逻辑注册为 typer 命令。"""

import typer
from nltlog import getLogger

from .brew import BrewInstall
from .code_server import CodeServerInstall
from .frpc import FrpcInstall
from .go import GoInstall
from .mcphub import FunMcpHub
from .newapi import FunNewApi
from .nodejs import NodeJSInstall
from .onehub import FunOneHub
from .ossutil import OSSUtilInstall
from .uif import UIFInstall
from .v2rayA import V2RayAInstall

logger = getLogger("funinstall")

app = typer.Typer(help="安装各类开发工具")


@app.command(name="code-server", help="安装 code-server（基于浏览器的 VS Code）")
def install_code_server() -> bool:
    """安装 code-server。"""
    logger.info("开始安装 code-server")
    return CodeServerInstall().install()


@app.command(name="go", help="安装 Go 语言环境")
def install_go(
    version: str = typer.Option(None, "--version", "-v", help="Go 版本，如 1.21.0"),
    force: bool = typer.Option(False, "--force", "-f", help="强制重新安装"),
) -> bool:
    """安装指定版本的 Go 语言。"""
    logger.info(f"开始安装 Go (version={version}, force={force})")
    return GoInstall(version=version, force=force).install()


@app.command(name="new-api", help="安装 new-api（OpenAI API 管理与分发系统）")
def install_newapi() -> bool:
    """安装 new-api。"""
    logger.info("开始安装 new-api")
    return FunNewApi().install()


@app.command(name="nodejs", help="安装 Node.js 运行环境")
def install_nodejs(
    version: str = typer.Option(
        None, "--version", "-v", help="nodejs 版本，如 18.17.0"
    ),
    latest: bool = typer.Option(False, "--latest", "-l", help="是否安装最新版本"),
    update: bool = typer.Option(False, "--update", "-u", help="是否更新版本"),
    force: bool = typer.Option(False, "--force", "-f", help="强制重新安装"),
) -> bool:
    """安装指定版本的 Node.js。"""
    logger.info(
        f"开始安装 NodeJS (version={version}, latest={latest}, update={update}, force={force})"
    )
    return NodeJSInstall(
        version=version, lasted=latest, update=update, force=force
    ).install()


@app.command(name="brew", help="安装 Homebrew 包管理器（macOS）")
def install_brew() -> bool:
    """安装 Homebrew。"""
    logger.info("开始安装 brew")
    return BrewInstall().install()


@app.command(name="v2rayA", help="安装 v2rayA 代理客户端")
def install_v2rayA() -> bool:
    """安装 v2rayA。"""
    logger.info("开始安装 v2rayA")
    return V2RayAInstall().install()


@app.command(name="frpc", help="安装 frpc 内网穿透客户端")
def install_frpc() -> bool:
    """安装 frpc。"""
    logger.info("开始安装 frpc")
    return FrpcInstall().install()


@app.command(name="mcphub", help="安装 MCP Hub 服务")
def install_mcphub() -> bool:
    """安装 MCP Hub。"""
    logger.info("开始安装 MCP Hub")
    return FunMcpHub().install()


@app.command(name="uif", help="安装 UIF（UI for Freedom）代理工具")
def install_uif() -> bool:
    """安装 UIF。"""
    logger.info("开始安装 UIF")
    return UIFInstall().install()


@app.command(name="onehub", help="安装 OneHub（API 聚合管理平台）")
def install_onehub() -> bool:
    """安装 OneHub。"""
    logger.info("开始安装 OneHub")
    return FunOneHub().install()


@app.command(name="ossutil", help="安装阿里云 OSS 命令行工具")
def install_ossutil() -> bool:
    """安装 ossutil。"""
    logger.info("开始安装 ossutil")
    return OSSUtilInstall().install()
