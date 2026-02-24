from funserver.servers.base.install import BaseInstall

from .utils import run_script_from_url


class FrpcInstall(BaseInstall):
    def __init__(self, version: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version

    def install_linux(self, *args, **kwargs) -> bool:
        """https://github.com/farfarfun/funfrp/tree/master/src/funfrp/frpc"""
        run_script_from_url(
            "https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_install.sh",
            script_name="funinstall_frpc.sh",
            chmod=True,
        )
        return True

    def uninstall_linux(self, *args, **kwargs) -> bool:
        run_script_from_url(
            "https://raw.githubusercontent.com/stilleshan/frpc/master/frpc_linux_uninstall.sh",
            script_name="funinstall_frpc.sh",
            chmod=True,
        )
        return True
