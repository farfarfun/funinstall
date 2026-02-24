"""new-api 安装模块。

new-api 是 OpenAI API 的管理与分发系统，支持多平台部署。
通过 GitHub Releases 获取最新构建产物并安装到 ~/opt/new-api/ 目录。
参考: https://github.com/QuantumNous/new-api
"""

from __future__ import annotations

import os

import requests
from funshell import run_shell_list
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

logger = getLogger("funinstall")


class NewApiInstall(BaseInstall):
    """new-api 安装器，从 GitHub Releases 下载对应平台的可执行文件。

    Args:
        overwrite: 是否覆盖已有安装。
    """

    def __init__(self, overwrite=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overwrite = overwrite

    def get_download_url(self) -> dict[str, str]:
        """从 GitHub API 获取最新 Release 的各资产下载链接。

        Returns:
            字典，键为资产文件名，值为对应的下载 URL。
        """
        url = "https://api.github.com/repos/QuantumNous/new-api/releases/latest"
        logger.info(f"正在从 {url} 获取最新版本信息")
        response = requests.get(url).json()
        assets = {
            asset["name"]: asset["browser_download_url"] for asset in response["assets"]
        }
        logger.debug(f"获取到 {len(assets)} 个资产文件")
        return assets

    def _install(self, device="one-api", *args, **kwargs) -> bool:
        """下载并安装指定平台的 new-api 可执行文件。

        Args:
            device: 资产文件名，用于从下载链接字典中匹配对应平台的产物。
        """
        root = f"{os.environ.get('HOME')}/opt/new-api"
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
        logger.success(f"成功安装 new-api 到 {root}")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """在 Linux 上安装 new-api。"""
        logger.info("开始在 Linux 上安装 new-api")
        return self._install("one-api", *args, **kwargs)

    def install_macos(self, *args, **kwargs) -> bool:
        """在 macOS 上安装 new-api。"""
        logger.info("开始在 macOS 上安装 new-api")
        return self._install("one-api-macos", *args, **kwargs)

    def install_windows(self, *args, **kwargs) -> bool:
        """在 Windows 上安装 new-api。"""
        logger.info("开始在 Windows 上安装 new-api")
        return self._install("one-api.exe", *args, **kwargs)
