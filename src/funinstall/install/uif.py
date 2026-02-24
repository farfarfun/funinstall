"""UIF（UI for Freedom）代理工具安装模块。

仅支持 Linux 平台，使用官方一键安装脚本并注册为 systemd 服务。
参考: https://ui4freedom.org/UIF_help/docs/install/linux
"""

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class UIFInstall(BaseInstall):
    """UIF 安装器，通过官方脚本在 Linux 上安装并配置 systemd 服务。"""

    def install_linux(self, *args, **kwargs) -> bool:
        """在 Linux 上安装 UIF 并设置开机自启动。"""
        logger.info("开始在 Linux 上安装 UIF")
        run_script_from_url(
            "https://fastly.jsdelivr.net/gh/UIforFreedom/UIF@master/uifd/linux_install.sh",
            script_name="funinstall_uif.sh",
            chmod=True,
        )
        logger.info("设置 ui4freedom 开机自启动")
        run_shell("sudo systemctl enable ui4freedom")
        logger.info("启动 ui4freedom 服务")
        run_shell("sudo systemctl restart ui4freedom")
        logger.success("成功安装 UIF")
        return True
