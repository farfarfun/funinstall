import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command, run_script_from_url

logger = getLogger("funinstall")

_SKIP_MSG = "Go 已安装，跳过安装。如需重新安装，请使用 force=True 参数"


class GoInstall(BaseInstall):
    def __init__(self, version: str = "", force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.force = force

    def is_installed(self) -> bool:
        return check_command("go version", "Go")

    def install_macos(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        run_shell("brew install go")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """https://github.com/Jrohy/go-install"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        version_args = f"-v {self.version}" if self.version else ""
        run_script_from_url(
            "https://go-install.netlify.app/install.sh",
            script_name="funinstall_go.sh",
            args=version_args,
        )
        logger.success(f"成功安装 Go {self.version or ''}")
        run_shell("sudo ln -fs /usr/local/go/bin/go /usr/local/bin/go")
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        try:
            arch = platform.machine().lower()
            arch_suffix = {
                "amd64": "amd64",
                "x86_64": "amd64",
                "i386": "386",
                "i686": "386",
                "x86": "386",
            }.get(arch)
            if not arch_suffix:
                logger.error(f"不支持的架构: {arch}")
                return False

            version = self.version or "1.21.0"
            filename = f"go{version}.windows-{arch_suffix}.msi"
            download_url = f"https://golang.org/dl/{filename}"
            install_dir = os.path.expanduser("~/Downloads")

            logger.info(f"开始下载 Go {version} for Windows {arch_suffix}")
            for cmd in [
                f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile {install_dir}\\{filename}"',
                f"powershell -Command \"Start-Process msiexec.exe -Wait -ArgumentList '/i {install_dir}\\{filename} /quiet'\"",
                f'powershell -Command "Remove-Item {install_dir}\\{filename}"',
            ]:
                run_shell(cmd)

            logger.success(f"成功安装 Go {version}")
            logger.info("请重新打开命令行窗口以使环境变量生效")
            return True
        except Exception as e:
            logger.error(f"安装 Go 失败: {e}")
            logger.info("Windows安装失败，请手动下载安装: https://golang.org/dl/")
            return False
