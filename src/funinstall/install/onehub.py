"""OneHub 安装与服务管理模块。

OneHub 是一个 API 聚合管理平台（MartialBE/one-hub 的二次开发）。
通过 GitHub Releases 获取最新构建产物并安装到 ~/opt/one-hub/ 目录，
同时作为 BaseServer 提供 start / stop / status 等服务管理能力。
参考: https://github.com/MartialBE/one-hub
"""

import os
from typing import Optional

import requests
from funshell import run_shell_list
from nltlog import getLogger

from funserver.servers.base import BaseServer, server_parser

logger = getLogger("funinstall")


class FunOneHub(BaseServer):
    """OneHub 安装器与服务管理器。

    继承自 BaseServer，同时提供安装和运行管理功能。
    默认端口 8801，服务名 funonehub。

    Args:
        overwrite: 是否覆盖已有安装。
    """

    def __init__(self, overwrite: bool = False, *args, **kwargs):
        super().__init__(server_name="funonehub", port=8801)
        self.overwrite = overwrite

    def update(self, args=None, **kwargs):
        """通过 pip 更新 funserver 依赖。"""
        logger.info("正在更新 funserver 依赖")
        run_shell_list(["pip install -U funserver"])

    def run_cmd(self, *args, **kwargs) -> Optional[str]:
        """构建 OneHub 的启动命令。

        Returns:
            启动命令字符串；若安装目录或配置文件不存在则返回 None。
        """
        root = f"{os.environ['HOME']}/opt/one-hub"
        if not os.path.exists(root):
            logger.warning(f"安装目录不存在: {root}")
            return None
        if not os.path.exists(f"{root}/config.yaml"):
            logger.warning(f"配置文件不存在: {root}/config.yaml")
            return None
        logger.debug(f"OneHub 启动命令: {root}/one-api --config {root}/config.yaml")
        return f"{root}/one-api --config {root}/config.yaml"

    def get_download_url(self) -> dict[str, str]:
        """从 GitHub API 获取最新 Release 的各资产下载链接。

        Returns:
            字典，键为资产文件名，值为对应的下载 URL。
        """
        url = "https://api.github.com/repos/MartialBE/one-hub/releases/latest"
        logger.info(f"正在从 {url} 获取最新版本信息")
        response = requests.get(url).json()
        assets = {
            asset["name"]: asset["browser_download_url"] for asset in response["assets"]
        }
        logger.debug(f"获取到 {len(assets)} 个资产文件")
        return assets

    def _install(self, device="one-api", *args, **kwargs) -> bool:
        """下载并安装指定平台的 OneHub 可执行文件。

        Args:
            device: 资产文件名，用于从下载链接字典中匹配对应平台的产物。
        """
        root = f"{os.environ.get('HOME')}/opt/one-hub"
        if not os.path.exists(root):
            logger.info(f"安装目录 {root} 不存在，正在创建")
            os.makedirs(root, exist_ok=True)

        download_url = self.get_download_url()[device]
        logger.info(f"正在下载 {device}: {download_url}")
        run_shell_list(
            [
                f"cd {root}",
                f"curl -L -o one-api {download_url}",
                "chmod u+x one-api",
            ]
        )
        logger.success(f"成功安装 OneHub 到 {root}")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """在 Linux 上安装 OneHub。"""
        logger.info("开始在 Linux 上安装 OneHub")
        return self._install("one-api", *args, **kwargs)

    def install_macos(self, *args, **kwargs) -> bool:
        """在 macOS 上安装 OneHub。"""
        logger.info("开始在 macOS 上安装 OneHub")
        return self._install("one-api-macos", *args, **kwargs)

    def install_windows(self, *args, **kwargs) -> bool:
        """在 Windows 上安装 OneHub。"""
        logger.info("开始在 Windows 上安装 OneHub")
        return self._install("one-api.exe", *args, **kwargs)


def funonehub():
    """funonehub CLI 入口函数，由 pyproject.toml [project.scripts] 调用。"""
    app = server_parser(FunOneHub())
    app()
