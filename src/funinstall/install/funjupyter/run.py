"""JupyterLab 服务管理模块。

将 JupyterLab 封装为 BaseServer，使用项目内置的 config.py 作为启动配置。
"""

import os.path

from funshell import run_shell_list
from funserver.servers.base import BaseServer, server_parser
from nltlog import getLogger

logger = getLogger("funinstall")


class FunJupyter(BaseServer):
    """JupyterLab 服务管理器。

    使用同目录下的 config.py 作为 JupyterLab 配置文件启动。
    """

    def __init__(self):
        super().__init__(server_name="funjupyter")

    def update(self, args=None, **kwargs):
        """通过 pip 更新 JupyterLab 到最新版本。"""
        logger.info("正在更新 JupyterLab")
        run_shell_list(["pip install -U jupyterlab"])

    def run_cmd(self, *args, **kwargs):
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


def funjupyter():
    """funjupyter CLI 入口函数。"""
    server = FunJupyter()
    parser = server_parser(server)
    args = parser.parse_args()
    params = vars(args)
    args.func(**params)
