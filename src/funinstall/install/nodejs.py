import os
import platform

from funbuild.shell import run_shell
from funserver.servers.base.install import BaseInstall

from funutil import getLogger


logger = getLogger("funinstall")


class NodeJSInstall(BaseInstall):
    def __init__(
        self, version=None, lasted=False, update=False, force=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.version = version
        self.lasted = lasted
        self.update = update
        self.force = force

    def is_installed(self) -> bool:
        """
        检查NodeJS是否已安装
        """
        try:
            # 检查系统路径中的node
            run_shell("node --version")
            logger.info("检测到系统中已安装 NodeJS")
            return True
        except:
            pass

        return False

    def install_macos(self, *args, **kwargs) -> bool:
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("NodeJS 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        run_shell("brew install nodejs")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装NodeJS
        https://github.com/Jrohy/nodejs-install
        """
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("NodeJS 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        run_shell(
            "curl -L -o funinstall_nodejs.sh https://nodejs-install.netlify.app/install.sh"
        )
        if self.version:
            run_shell(f"sudo bash funinstall_nodejs.sh -v {self.version}")
            logger.success(f"成功安装 nodeJs {self.version}")
        elif self.lasted:
            run_shell("sudo bash funinstall_nodejs.sh -l")
            logger.success("成功安装 nodeJs")
        elif self.update:
            run_shell("sudo bash funinstall_nodejs.sh -f")
            logger.success("成功更新 nodeJs")
        else:
            run_shell("sudo bash funinstall_nodejs.sh")
            logger.success("成功安装 nodeJs")
        run_shell("rm funinstall_nodejs.sh")
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        """
        在Windows系统上安装NodeJS
        使用官方安装包进行安装
        """
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("NodeJS 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        try:
            # 检测架构
            arch = platform.machine().lower()
            if arch in ["amd64", "x86_64"]:
                arch_suffix = "x64"
            elif arch in ["i386", "i686", "x86"]:
                arch_suffix = "x86"
            else:
                logger.error(f"不支持的架构: {arch}")
                return False

            # 如果没有指定版本，使用默认版本
            version = self.version if self.version else "18.17.0"

            # 构建下载URL
            filename = f"node-v{version}-{arch_suffix}.msi"
            download_url = f"https://nodejs.org/dist/v{version}/{filename}"

            logger.info(f"开始下载 NodeJS {version} for Windows {arch_suffix}")

            # Windows安装目录
            install_dir = os.path.expanduser("~/Downloads")

            # 下载安装包
            commands = [
                f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile {install_dir}\\{filename}"',
                f"powershell -Command \"Start-Process msiexec.exe -Wait -ArgumentList '/i {install_dir}\\{filename} /quiet'\"",
                f'powershell -Command "Remove-Item {install_dir}\\{filename}"',
            ]

            for cmd in commands:
                run_shell(cmd)

            logger.success(f"成功安装 NodeJS {version}")
            logger.info("请重新打开命令行窗口以使环境变量生效")
            return True

        except Exception as e:
            logger.error(f"安装 NodeJS 失败: {e}")
            logger.info("Windows安装失败，请手动下载安装:")
            logger.info("下载地址: https://nodejs.org/")
            return False
