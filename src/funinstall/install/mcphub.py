import os
from typing import Optional

import requests
from funshell import run_shell_list, kill_process
from nltlog import getLogger

from funserver.servers.base import BaseServer, server_parser

logger = getLogger("funinstall")


class FunMcpHub(BaseServer):
    def __init__(self, overwrite: bool = False, *args, **kwargs):
        super().__init__(server_name="funmcphub", port=3000)
        self.overwrite = overwrite

    def update(self, args=None, **kwargs):
        run_shell_list(["pip install -U funserver"])

    def run_cmd(self, *args, **kwargs) -> Optional[str]:
        root = f"{os.environ['HOME']}/opt/mcp-hub"
        if not os.path.exists(root):
            logger.warning(f"{root} not exists")
            return None
        return f"{root}/mcphub"

    def _install(self, device="mcp-hub", *args, **kwargs) -> bool:
        root = f"{os.environ.get('HOME')}/opt/mcp-hub"
        if not os.path.exists(root):
            logger.info(f"目录{root}不存在，创建")
            os.makedirs(root, exist_ok=True)

        run_shell_list(["npm install -g @samanhappy/mcphub"])
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        return self._install("mcp-hub", *args, **kwargs)

    def install_macos(self, *args, **kwargs) -> bool:
        return self._install("mcp-hub", *args, **kwargs)


def funmcphub():
    app = server_parser(FunMcpHub())
    app()
