import os
import platform

from funbuild.shell import run_shell
from funserver.servers.base.install import BaseInstall
from funutil import getLogger


logger = getLogger("funinstall")


class GoInstall(BaseInstall):
    def __init__(self, version: str = "", force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.force = force

    def is_installed(self) -> bool:
        """
        检查Go是否已安装
        """
        try:
            # 检查系统路径中的go
            run_shell("go version")
            logger.info("检测到系统中已安装 Go")
            return True
        except:
            pass

        return False

    def install_macos(self, *args, **kwargs) -> bool:
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("Go 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        run_shell("brew install go")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装go
        https://github.com/Jrohy/go-install
        """
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("Go 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        run_shell(
            "curl -L -o funinstall_go.sh https://go-install.netlify.app/install.sh"
        )
        if self.version:
            run_shell(f"sudo bash funinstall_go.sh -v {self.version}")
            logger.success(f"成功安装 Go {self.version}")
        else:
            run_shell("sudo bash funinstall_go.sh")
            logger.success("成功安装 Go")
        run_shell("rm funinstall_go.sh")
        run_shell("sudo ln -fs /usr/local/go/bin/go /usr/local/bin/go")
        return True

    def install_windows(self, *args, **kwargs) -> bool:
        """
        在Windows系统上安装Go语言
        使用官方安装包进行安装
        """
        # 检查是否已安装
        if not self.force and self.is_installed():
            logger.info("Go 已安装，跳过安装。如需重新安装，请使用 force=True 参数")
            return True

        try:
            # 检测架构
            arch = platform.machine().lower()
            if arch in ["amd64", "x86_64"]:
                arch_suffix = "amd64"
            elif arch in ["i386", "i686", "x86"]:
                arch_suffix = "386"
            else:
                logger.error(f"不支持的架构: {arch}")
                return False

            # 如果没有指定版本，使用默认版本
            version = self.version if self.version else "1.21.0"

            # 构建下载URL
            filename = f"go{version}.windows-{arch_suffix}.msi"
            download_url = f"https://golang.org/dl/{filename}"

            logger.info(f"开始下载 Go {version} for Windows {arch_suffix}")

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

            logger.success(f"成功安装 Go {version}")
            logger.info("请重新打开命令行窗口以使环境变量生效")
            return True

        except Exception as e:
            logger.error(f"安装 Go 失败: {e}")
            logger.info("Windows安装失败，请手动下载安装:")
            logger.info("下载地址: https://golang.org/dl/")
            return False
