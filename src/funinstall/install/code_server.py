"""code-server 安装模块。

code-server 是基于浏览器的 VS Code，支持远程开发。
仅支持 Linux 平台，使用官方一键安装脚本。
参考: https://github.com/coder/code-server
"""

from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class CodeServerInstall(BaseInstall):
    """code-server 安装器，通过官方脚本在 Linux 上安装。"""

    def install_linux(self, *args, **kwargs) -> bool:
        """使用官方一键脚本安装 code-server。"""
        logger.info("开始在 Linux 上安装 code-server")
        run_script_from_url(
            "https://code-server.dev/install.sh",
            script_name="funinstall_cs.sh",
        )
        logger.success("成功安装 code-server")
        return True
