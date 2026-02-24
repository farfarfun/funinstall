"""Go 语言环境安装模块。

支持 Linux（一键脚本）、macOS（brew）、Windows（官方 MSI 安装包）三个平台。
- Linux 参考: https://github.com/Jrohy/go-install
- Windows 参考: https://golang.org/dl/
"""

import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command, run_script_from_url

logger = getLogger("funinstall")

_SKIP_MSG = "Go 已安装，跳过安装。如需重新安装，请使用 force=True 参数"


class GoInstall(BaseInstall):
    """Go 语言安装器，支持 Linux / macOS / Windows 三平台。

    Args:
        version: 指定安装版本，如 ``1.21.0``；留空则安装默认版本。
        force: 为 True 时即使已安装也会重新安装。
    """

    def __init__(self, version: str = "", force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.force = force

    def is_installed(self) -> bool:
        """检查系统中是否已安装 Go。"""
        return check_command("go version", "Go")

    def install_macos(self, *args, **kwargs) -> bool:
        """通过 Homebrew 在 macOS 上安装 Go。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        logger.info("通过 brew 安装 Go")
        run_shell("brew install go")
        logger.success("成功在 macOS 上安装 Go")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """通过一键脚本在 Linux 上安装 Go。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        version_args = f"-v {self.version}" if self.version else ""
        logger.info(f"通过一键脚本安装 Go{' ' + self.version if self.version else ''}")
        run_script_from_url(
            "https://go-install.netlify.app/install.sh",
            script_name="funinstall_go.sh",
            args=version_args,
        )
        logger.info("创建符号链接 /usr/local/bin/go -> /usr/local/go/bin/go")
        run_shell("sudo ln -fs /usr/local/go/bin/go /usr/local/bin/go")
        logger.success(
            f"成功在 Linux 上安装 Go{' ' + self.version if self.version else ''}"
        )
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        """通过官方 MSI 安装包在 Windows 上安装 Go。"""
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
            logger.info(f"下载地址: {download_url}")
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
            logger.info("Windows 安装失败，请手动下载安装: https://golang.org/dl/")
            return False
