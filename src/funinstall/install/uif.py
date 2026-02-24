from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class UIFInstall(BaseInstall):
    def install_linux(self, *args, **kwargs) -> bool:
        """https://ui4freedom.org/UIF_help/docs/install/linux"""
        run_script_from_url(
            "https://fastly.jsdelivr.net/gh/UIforFreedom/UIF@master/uifd/linux_install.sh",
            script_name="funinstall_uif.sh",
            chmod=True,
        )
        run_shell("sudo systemctl enable ui4freedom")
        run_shell("sudo systemctl restart ui4freedom")
        logger.success("成功安装 UIF")
        return True
