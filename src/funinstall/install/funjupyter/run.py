"""JupyterLab 服务管理模块。

将 JupyterLab 封装为 BaseServer，使用项目内置的 config.py 作为启动配置。
"""

import os.path

from farlog import getLogger
from funserver.servers.base import BaseServer, server_parser
from funshell import run_shell_list

logger = getLogger("funinstall")


class FunJupyter(BaseServer):
    """JupyterLab 服务管理器。

    使用同目录下的 config.py 作为 JupyterLab 配置文件启动。
    """

    def __init__(self) -> None:
        super().__init__(server_name="funjupyter")

    def update(self, args: object | None = None, **kwargs: object) -> None:
        """通过 pip 更新 JupyterLab 到最新版本。"""
        logger.info("正在更新 JupyterLab")
        run_shell_list(["pip install -U jupyterlab"])

    def run_cmd(self, *args: object, **kwargs: object) -> str:
        """构建 JupyterLab 的启动命令，使用内置配置文件。

        Returns:
            JupyterLab 启动命令字符串。
        """
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config.py"
        )
        cmd = f"jupyter lab --config {config_path} --watch "
        logger.debug(f"JupyterLab 启动命令: {cmd}")
        return cmd


def funjupyter() -> None:
    """funjupyter CLI 入口函数。"""
    app = server_parser(FunJupyter())
    app()
