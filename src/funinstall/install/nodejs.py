import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command, run_script_from_url

logger = getLogger("funinstall")

_SKIP_MSG = "NodeJS 已安装，跳过安装。如需重新安装，请使用 force=True 参数"


class NodeJSInstall(BaseInstall):
    def __init__(
        self, version=None, lasted=False, update=False, force=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.version = version
        self.latest = lasted
        self.update = update
        self.force = force

    def is_installed(self) -> bool:
        return check_command("node --version", "NodeJS")

    def install_macos(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        run_shell("brew install nodejs")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """https://github.com/Jrohy/nodejs-install"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        if self.version:
            args_str = f"-v {self.version}"
        elif self.latest:
            args_str = "-l"
        elif self.update:
            args_str = "-f"
        else:
            args_str = ""

        run_script_from_url(
            "https://nodejs-install.netlify.app/install.sh",
            script_name="funinstall_nodejs.sh",
            args=args_str,
        )
        logger.success(f"成功安装 NodeJS {self.version or ''}")
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        try:
            arch = platform.machine().lower()
            arch_suffix = {
                "amd64": "x64",
                "x86_64": "x64",
                "i386": "x86",
                "i686": "x86",
                "x86": "x86",
            }.get(arch)
            if not arch_suffix:
                logger.error(f"不支持的架构: {arch}")
                return False

            version = self.version or "18.17.0"
            filename = f"node-v{version}-{arch_suffix}.msi"
            download_url = f"https://nodejs.org/dist/v{version}/{filename}"
            install_dir = os.path.expanduser("~/Downloads")

            logger.info(f"开始下载 NodeJS {version} for Windows {arch_suffix}")
            for cmd in [
                f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile {install_dir}\\{filename}"',
                f"powershell -Command \"Start-Process msiexec.exe -Wait -ArgumentList '/i {install_dir}\\{filename} /quiet'\"",
                f'powershell -Command "Remove-Item {install_dir}\\{filename}"',
            ]:
                run_shell(cmd)

            logger.success(f"成功安装 NodeJS {version}")
            logger.info("请重新打开命令行窗口以使环境变量生效")
            return True
        except Exception as e:
            logger.error(f"安装 NodeJS 失败: {e}")
            logger.info("Windows安装失败，请手动下载安装: https://nodejs.org/")
            return False
