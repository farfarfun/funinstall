from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import run_script_from_url

logger = getLogger("funinstall")


class BrewInstall(BaseInstall):
    def install_linux(self, *args, **kwargs) -> bool:
        return False

    def install_macos(self, *args, **kwargs) -> bool:
        """https://github.com/Jrohy/go-install"""
        run_script_from_url(
            "https://gitee.com/ineo6/homebrew-install/raw/master/install.sh",
            script_name="funinstall_brew.sh",
        )
        logger.success("成功安装 brew")
        return True
