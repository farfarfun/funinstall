"""Homebrew 包管理器安装模块。

仅支持 macOS，使用 ineo6 维护的国内镜像安装脚本。
参考: https://gitee.com/ineo6/homebrew-install
"""

from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class BrewInstall(BaseInstall):
    """Homebrew 安装器，通过远程脚本在 macOS 上安装 Homebrew。"""

    def install_linux(self, *args, **kwargs) -> bool:
        """Linux 暂不支持 Homebrew 安装。"""
        logger.warning("Homebrew 安装暂不支持 Linux 平台")
        return False

    def install_macos(self, *args, **kwargs) -> bool:
        """通过 ineo6 镜像脚本在 macOS 上安装 Homebrew。"""
        logger.info("开始在 macOS 上安装 Homebrew")
        run_script_from_url(
            "https://gitee.com/ineo6/homebrew-install/raw/master/install.sh",
            script_name="funinstall_brew.sh",
        )
        logger.success("成功安装 brew")
        return True
