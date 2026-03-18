"""new-api 安装与服务管理模块。

new-api 是 OpenAI API 的管理与分发系统，支持多平台部署。
通过 GitHub Releases 获取最新构建产物并安装到 ~/opt/new-api/ 目录，
同时作为 BaseServer 提供 start / stop / status 等服务管理能力。
参考: https://github.com/QuantumNous/new-api
"""

import os
import platform
from typing import Optional

import requests
from funshell import run_shell_list
from nltlog import getLogger

from funserver.servers.base import BaseServer, server_parser

logger = getLogger("funinstall")


class FunNewApi(BaseServer):
    """new-api 安装器与服务管理器。

    继承自 BaseServer，同时提供安装和运行管理功能。
    默认端口 8806，服务名 funnewapi。

    Args:
        overwrite: 是否覆盖已有安装。
    """

    def __init__(self, overwrite: bool = False, *args, **kwargs):
        super().__init__(server_name="funnewapi", port=8801, *args, **kwargs)
        self.overwrite = overwrite

    @property
    def run_path(self):
        return f"{os.environ['HOME']}/opt/new-api"

    def run_cmd(self, *args, **kwargs) -> Optional[str]:
        """构建 new-api 的启动命令。

        Returns:
            启动命令字符串；若安装目录或可执行文件不存在则返回 None。
        """
        root = self.run_path
        if not os.path.exists(root):
            logger.warning(f"安装目录不存在: {root}")
            return None
        env_file = f"{root}/.env"
        if not os.path.exists(env_file):
            logger.warning(f"配置文件不存在: {env_file}")
            return None

        executable = (
            f"{root}/new-api.exe"
            if platform.system() == "Windows"
            else f"{root}/new-api"
        )
        if not os.path.exists(executable):
            logger.warning(f"可执行文件不存在: {executable}")
            return None
        cmd = executable
        logger.debug(f"new-api 启动命令: {cmd}")
        return cmd

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

    def _select_asset_name(self, assets: dict[str, str], *, system: str) -> str:
        system = system.lower()

        def pick(predicate):
            matches = [name for name in assets.keys() if predicate(name)]
            if not matches:
                raise KeyError(
                    f"未找到匹配的安装包资产: system={system}, assets={list(assets.keys())}"
                )
            matches.sort()
            return matches[-1]

        if system == "windows":
            return pick(lambda n: n.startswith("new-api-") and n.endswith(".exe"))

        if system == "darwin":
            machine = platform.machine().lower()
            if machine in {"arm64", "aarch64"}:
                return pick(
                    lambda n: n.startswith("new-api-arm64-") and not n.endswith(".exe")
                )
            return pick(
                lambda n: n.startswith("new-api-macos-") and not n.endswith(".exe")
            )

        return pick(
            lambda n: (
                n.startswith("new-api-")
                and ("macos" not in n)
                and ("arm64" not in n)
                and (not n.endswith(".exe"))
            )
        )

    def _install(self, system: Optional[str] = None, *args, **kwargs) -> bool:
        """下载并安装指定平台的 new-api 可执行文件。

        Args:
            system: 指定系统类型（默认自动识别），用于选择对应平台的产物。
        """
        root = self.run_path
        if not os.path.exists(root):
            logger.info(f"安装目录 {root} 不存在，正在创建")
            os.makedirs(root, exist_ok=True)

        sys_name = system or platform.system()
        assets = self.get_download_url()
        asset_name = self._select_asset_name(assets, system=sys_name)
        download_url = assets[asset_name]
        logger.info(f"正在下载 {asset_name}: {download_url}")

        output_name = "new-api.exe" if sys_name.lower() == "windows" else "new-api"
        run_shell_list(
            [
                f"cd {root}",
                f"curl -L -o {output_name} {download_url}",
                f"chmod u+x {output_name}"
                if output_name != "new-api.exe"
                else "echo skip chmod on windows",
            ]
        )
        logger.success(f"成功安装 new-api 到 {root}")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """在 Linux 上安装 new-api。"""
        logger.info("开始在 Linux 上安装 new-api")
        return self._install("Linux", *args, **kwargs)

    def install_macos(self, *args, **kwargs) -> bool:
        """在 macOS 上安装 new-api。"""
        logger.info("开始在 macOS 上安装 new-api")
        return self._install("Darwin", *args, **kwargs)

    def install_windows(self, *args, **kwargs) -> bool:
        """在 Windows 上安装 new-api。"""
        logger.info("开始在 Windows 上安装 new-api")
        return self._install("Windows", *args, **kwargs)


def funnewapi():
    """funnewapi CLI 入口函数，由 pyproject.toml [project.scripts] 调用。"""
    app = server_parser(FunNewApi())
    app()
