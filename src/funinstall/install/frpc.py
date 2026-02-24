"""frpc 内网穿透客户端安装/卸载模块。

frpc 是 frp 项目的客户端，用于将内网服务暴露到公网。
仅支持 Linux 平台，使用 stilleshan 维护的一键脚本。
参考: https://github.com/stilleshan/frpc
"""

from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class FrpcInstall(BaseInstall):
    """frpc 安装器，支持 Linux 平台的安装与卸载。"""

    def __init__(self, version: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version

    def install_linux(self, *args, **kwargs) -> bool:
        """通过一键脚本在 Linux 上安装 frpc。"""
        logger.info("开始在 Linux 上安装 frpc")
        run_script_from_url(
            "https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_install.sh",
            script_name="funinstall_frpc.sh",
            chmod=True,
        )
        logger.success("成功安装 frpc")
        return True

    def uninstall_linux(self, *args, **kwargs) -> bool:
        """通过一键脚本在 Linux 上卸载 frpc。"""
        logger.info("开始卸载 frpc")
        run_script_from_url(
            "https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_uninstall.sh",
            script_name="funinstall_frpc.sh",
            chmod=True,
        )
        logger.success("成功卸载 frpc")
        return True
