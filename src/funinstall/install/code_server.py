from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class CodeServerInstall(BaseInstall):
    def install_linux(self, *args, **kwargs) -> bool:
        """https://github.com/coder/code-server"""
        run_script_from_url(
            "https://code-server.dev/install.sh",
            script_name="funinstall_cs.sh",
        )
        logger.success("成功安装 code-server")
        return True
