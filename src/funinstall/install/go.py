from funbuild.shell import run_shell
from funutil import getLogger

from .base import install_app as app

logger = getLogger("funinstall")


@app.command()
def install_go(version=None) -> bool:
    """
    https://github.com/Jrohy/go-install
    """

    if version:
        run_shell(
            f"source <(curl -L https://go-install.netlify.app/install.sh) -v {version}"
        )
        logger.success(f"成功安装 Go {version}")
        return True

    run_shell("source <(curl -L https://go-install.netlify.app/install.sh)")
    logger.success("成功安装 Go")
    return True
