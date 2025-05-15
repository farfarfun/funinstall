import typer
from funbuild.shell import run_shell
from funutil import getLogger

from .base import install_app as app

logger = getLogger("funinstall")


@app.command(name="go")
def install_go(
    version: str = typer.Option(None, "--version", "-v", help="Go 版本"),
) -> bool:
    """
    使用一键脚本安装go
    https://github.com/Jrohy/go-install

    """
    run_shell("curl -L -o funinstall_go.sh https://go-install.netlify.app/install.sh")
    if version:
        run_shell(f'sudo bash funinstall_go.sh -v {version}"')
        logger.success(f"成功安装 Go {version}")
    else:
        run_shell("sudo bash funinstall_go.sh")
        logger.success("成功安装 Go")
    run_shell("rm funinstall_go.sh")
    return True
