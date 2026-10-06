"""MCP Hub 安装与服务管理模块。

MCP Hub 通过 npm 全局安装 @samanhappy/mcphub 包。
同时作为 BaseServer 提供 start / stop / status 等服务管理能力。
参考: https://www.npmjs.com/package/@samanhappy/mcphub
"""

import os

from funshell import run_shell_list
from farlog import getLogger

from funserver.servers.base import BaseServer, server_parser

from .utils import ensure_command_succeeds

logger = getLogger("funinstall")


class FunMcpHub(BaseServer):
    """MCP Hub 安装器与服务管理器。

    继承自 BaseServer，同时提供安装和运行管理功能。
    默认端口 8802，服务名 funmcphub。

    Args:
        overwrite: 是否覆盖已有安装。
    """

    def __init__(self, overwrite: bool = False, *args: object, **kwargs: object) -> None:
        super().__init__(server_name="funmcphub", port=8802)
        self.overwrite = overwrite

    @property
    def run_path(self) -> str:
        return f"{os.environ['HOME']}/opt/mcp-hub"

    def update(self, args: object | None = None, **kwargs: object) -> None:
        """通过 pip 更新 funserver 依赖。"""
        logger.info("正在更新 funserver 依赖")
        run_shell_list(["pip install -U funserver"])

    def run_cmd(self, *args: object, **kwargs: object) -> str | None:
        """返回 MCP Hub 的启动命令。"""
        logger.debug("MCP Hub 启动命令: mcphub")
        return "mcphub"

    def _install(
        self, device: str = "mcp-hub", *args: object, **kwargs: object
    ) -> bool:
        """通过 npm 全局安装 MCP Hub。

        Args:
            device: 安装目标标识（预留参数，当前未区分平台）。
        """
        root = self.run_path
        if not os.path.exists(root):
            logger.info(f"安装目录 {root} 不存在，正在创建")
            os.makedirs(root, exist_ok=True)

        logger.info("通过 npm 全局安装 @samanhappy/mcphub")
        command = "npm install -g @samanhappy/mcphub"
        ensure_command_succeeds(run_shell_list([command]), command)
        logger.success("成功安装 MCP Hub")
        return True

    def install_linux(self, *args: object, **kwargs: object) -> bool:
        """在 Linux 上安装 MCP Hub。"""
        logger.info("开始在 Linux 上安装 MCP Hub")
        return self._install("mcp-hub", *args, **kwargs)

    def install_macos(self, *args: object, **kwargs: object) -> bool:
        """在 macOS 上安装 MCP Hub。"""
        logger.info("开始在 macOS 上安装 MCP Hub")
        return self._install("mcp-hub", *args, **kwargs)


def funmcphub() -> None:
    """funmcphub CLI 入口函数，由 pyproject.toml [project.scripts] 调用。"""
    app = server_parser(FunMcpHub())
    app()
