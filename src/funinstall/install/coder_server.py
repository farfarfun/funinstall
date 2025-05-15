from funbuild.shell import run_shell
from funutil import getLogger

from .base import install_app as app

logger = getLogger("funinstall")


@app.command(name="code-server")
def install_code_server() -> bool:
    """
    使用一键脚本安装code-server
    https://github.com/coder/code-server
    """
    run_shell("curl -L -o funinstall_cs.sh https://code-server.dev/install.sh")
    run_shell("sudo bash funinstall_cs.sh")
    logger.success("成功安装 code-server")
    run_shell("rm funinstall_cs.sh")
    return True
