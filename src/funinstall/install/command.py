import typer

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

app = typer.Typer()


@app.command(name="code-server")
def install_code_server() -> bool:
    return CodeServerInstall().install()


@app.command(name="go")
def install_go(
    version: str = typer.Option(None, "--version", "-v", help="Go 版本"),
    force: bool = typer.Option(False, "--force", "-f", help="强制重新安装"),
) -> bool:
    return GoInstall(version=version, force=force).install()


@app.command(name="new-api")
def install_newapi() -> bool:
    return NewApiInstall().install()


@app.command(name="nodejs")
def install_nodejs(
    version: str = typer.Option(None, "--version", "-v", help="nodejs 版本"),
    latest: bool = typer.Option(False, "--latest", "-l", help="是否安装最新版本"),
    update: bool = typer.Option(False, "--update", "-u", help="是否更新版本"),
    force: bool = typer.Option(False, "--force", "-f", help="强制重新安装"),
) -> bool:
    return NodeJSInstall(
        version=version, lasted=latest, update=update, force=force
    ).install()


@app.command(name="brew")
def install_brew() -> bool:
    return BrewInstall().install()


@app.command(name="v2rayA")
def install_v2rayA() -> bool:
    return V2RayAInstall().install()


@app.command(name="frpc")
def install_frpc() -> bool:
    return FrpcInstall().install()


@app.command(name="mcphub")
def install_mcphub() -> bool:
    return FunMcpHub().install()


@app.command(name="uif")
def install_uif() -> bool:
    return UIFInstall().install()


@app.command(name="onehub")
def install_onehub() -> bool:
    return FunOneHub().install()


@app.command(name="ossutil")
def install_ossutil() -> bool:
    return OSSUtilInstall().install()
