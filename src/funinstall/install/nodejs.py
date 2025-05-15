import typer
from funbuild.shell import run_shell
from funutil import getLogger

from .base import install_app as app

logger = getLogger("funinstall")


@app.command(name="nodejs")
def install_nodejs(
    version: str = typer.Option(None, "--version", "-v", help="nodejs 版本"),
    lasted: bool = typer.Option(False, "--version", "-v", help="是否安装最新版本"),
    update: bool = typer.Option(False, "--version", "-v", help="是否更新版本"),
) -> bool:
    """
    使用一键脚本安装nodeJs
    https://github.com/Jrohy/nodejs-install
    """
    run_shell(
        "curl -L -o funinstall_nodejs.sh https://nodejs-install.netlify.app/install.sh"
    )
    if version:
        run_shell(f'sudo bash funinstall_nodejs.sh -v {version}"')
        logger.success(f"成功安装 nodeJs {version}")
    elif lasted:
        run_shell("sudo bash funinstall_nodejs.sh -l")
        logger.success("成功安装 nodeJs")
    elif update:
        run_shell("sudo bash funinstall_nodejs.sh -f")
        logger.success("成功更新 nodeJs")
    else:
        run_shell("sudo bash funinstall_nodejs.sh")
        logger.success("成功安装 nodeJs")
    run_shell("rm funinstall_nodejs.sh")
    return True
