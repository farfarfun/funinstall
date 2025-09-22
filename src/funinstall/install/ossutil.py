import os
import platform

from funbuild.shell import run_shell
from funserver.servers.base.install import BaseInstall

from funutil import getLogger


logger = getLogger("funinstall")


class OSSUtilInstall(BaseInstall):
    def __init__(self, version="2.1.2", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.base_url = "https://gosspublic.alicdn.com/ossutil/v2"
        self.install_path = "~/opt/bin/"

    def install_macos(self, *args, **kwargs) -> bool:
        """
        在macOS系统上安装ossutil
        支持x86_64和ARM64架构
        """
        try:
            # 检测架构
            arch = platform.machine().lower()
            if arch == "x86_64":
                arch_suffix = "amd64"
            elif arch == "arm64":
                arch_suffix = "arm64"
            else:
                logger.error(f"不支持的架构: {arch}")
                return False

            # 构建下载URL
            filename = f"ossutil-{self.version}-mac-{arch_suffix}.zip"
            download_url = f"{self.base_url}/{self.version}/{filename}"

            logger.info(f"开始下载 ossutil {self.version} for macOS {arch_suffix}")

            folder_name = f"ossutil-{self.version}-mac-{arch_suffix}"
            # 下载和安装
            commands = [
                f"mkdir {self.install_path}",
                f"curl -o {filename} {download_url}",
                f"unzip {filename}",
                f"cd {folder_name} && chmod 755 ossutil && mv ossutil {self.install_path}",
                f"cd .. && rm -rf {filename} {folder_name}",
            ]

            for cmd in commands:
                run_shell(cmd)

            # 验证安装
            run_shell("ossutil version")
            logger.success(f"成功安装 ossutil {self.version} 到 {self.install_path}")
            return True

        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_linux(self, *args, **kwargs) -> bool:
        """
        在Linux系统上安装ossutil
        支持x86_64、x86、ARM64、ARM32架构
        """
        try:
            # 检测架构
            arch = platform.machine().lower()
            if arch in ["x86_64", "amd64"]:
                arch_suffix = "amd64"
            elif arch in ["i386", "i686", "x86"]:
                arch_suffix = "386"
            elif arch in ["aarch64", "arm64"]:
                arch_suffix = "arm64"
            elif arch.startswith("arm"):
                arch_suffix = "arm"
            else:
                logger.error(f"不支持的架构: {arch}")
                return False

            # 构建下载URL
            filename = f"ossutil-{self.version}-linux-{arch_suffix}.zip"
            download_url = f"{self.base_url}/{self.version}/{filename}"

            logger.info(f"开始下载 ossutil {self.version} for Linux {arch_suffix}")

            folder_name = f"ossutil-{self.version}-linux-{arch_suffix}"
            # 下载和安装
            commands = [
                f"mkdir -p {self.install_path}",
                f"curl -o {filename} {download_url}",
                f"unzip {filename}",
                f"cd {folder_name} && chmod 755 ossutil && mv ossutil {self.install_path}/",
                f"cd .. && rm -rf {filename} {folder_name}",
            ]

            for cmd in commands:
                run_shell(cmd)

            # 验证安装
            run_shell(f"{self.install_path}/ossutil version")
            logger.success(f"成功安装 ossutil {self.version} 到 {self.install_path}")
            return True

        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_windows(self, *args, **kwargs) -> bool:
        """
        在Windows系统上安装ossutil
        支持x86_64和x86架构
        注意：Windows安装需要手动配置环境变量
        """
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

            # 构建下载URL
            filename = f"ossutil-{self.version}-windows-{arch_suffix}.zip"
            download_url = f"{self.base_url}/{self.version}/{filename}"

            # Windows安装目录
            install_dir = os.path.expanduser(f"{self.install_path}")

            logger.info(f"开始下载 ossutil {self.version} for Windows {arch_suffix}")
            logger.info(f"安装目录: {install_dir}")

            # 创建安装目录
            os.makedirs(install_dir, exist_ok=True)

            folder_name = f"ossutil-{self.version}-windows-{arch_suffix}"
            # 下载和解压（Windows需要使用PowerShell）
            commands = [
                f'powershell -Command "New-Item -ItemType Directory -Force -Path {install_dir}"',
                f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile {filename}"',
                f'powershell -Command "Expand-Archive -Path {filename} -DestinationPath . -Force"',
                f'powershell -Command "Move-Item {folder_name}\\ossutil.exe {install_dir}\\ossutil.exe"',
                f'powershell -Command "Remove-Item {filename}"',
                f'powershell -Command "Remove-Item {folder_name} -Recurse"',
            ]

            for cmd in commands:
                run_shell(cmd)

            logger.success(f"成功安装 ossutil {self.version} 到 {install_dir}")
            logger.info("请手动将以下路径添加到系统环境变量 PATH 中:")
            logger.info(f"  {install_dir}")
            logger.info("添加完成后，重新打开命令行窗口即可使用 ossutil 命令")

            return True

        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            logger.info("Windows安装失败，请手动下载安装:")
            logger.info(f"下载地址: {self.base_url}/{self.version}/")
            return False
