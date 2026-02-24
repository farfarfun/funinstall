"""Node.js 运行环境安装模块。

支持 Linux（一键脚本）、macOS（brew）、Windows（官方 MSI 安装包）三个平台。
- Linux 参考: https://github.com/Jrohy/nodejs-install
- Windows 参考: https://nodejs.org/
"""

import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command, run_script_from_url

logger = getLogger("funinstall")

_SKIP_MSG = "NodeJS 已安装，跳过安装。如需重新安装，请使用 force=True 参数"


class NodeJSInstall(BaseInstall):
    """Node.js 安装器，支持 Linux / macOS / Windows 三平台。

    Args:
        version: 指定安装版本，如 ``18.17.0``；留空则安装默认版本。
        lasted: 为 True 时安装最新版本（对应 CLI ``--latest``）。
        update: 为 True 时更新已有版本。
        force: 为 True 时即使已安装也会重新安装。
    """

    def __init__(
        self, version=None, lasted=False, update=False, force=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.version = version
        self.latest = lasted
        self.update = update
        self.force = force

    def is_installed(self) -> bool:
        """检查系统中是否已安装 Node.js。"""
        return check_command("node --version", "NodeJS")

    def install_macos(self, *args, **kwargs) -> bool:
        """通过 Homebrew 在 macOS 上安装 Node.js。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        logger.info("通过 brew 安装 NodeJS")
        run_shell("brew install nodejs")
        logger.success("成功在 macOS 上安装 NodeJS")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """通过一键脚本在 Linux 上安装 Node.js。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True

        if self.version:
            args_str = f"-v {self.version}"
            logger.info(f"指定版本安装 NodeJS {self.version}")
        elif self.latest:
            args_str = "-l"
            logger.info("安装最新版本 NodeJS")
        elif self.update:
            args_str = "-f"
            logger.info("更新 NodeJS 到最新版本")
        else:
            args_str = ""
            logger.info("安装 NodeJS 默认版本")

        run_script_from_url(
            "https://nodejs-install.netlify.app/install.sh",
            script_name="funinstall_nodejs.sh",
            args=args_str,
        )
        logger.success(
            f"成功在 Linux 上安装 NodeJS{' ' + self.version if self.version else ''}"
        )
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        """通过官方 MSI 安装包在 Windows 上安装 Node.js。"""
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
            logger.info(f"下载地址: {download_url}")
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
            logger.info("Windows 安装失败，请手动下载安装: https://nodejs.org/")
            return False
