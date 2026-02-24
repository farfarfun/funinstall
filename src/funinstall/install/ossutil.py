from __future__ import annotations

import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command

logger = getLogger("funinstall")

_SKIP_MSG = "ossutil 已安装，跳过安装。如需重新安装，请使用 force=True 参数"

ARCH_MAP_GENERIC = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "i386": "386",
    "i686": "386",
    "x86": "386",
}
ARCH_MAP_LINUX = {**ARCH_MAP_GENERIC, "aarch64": "arm64", "arm64": "arm64"}
ARCH_MAP_MAC = {"x86_64": "amd64", "arm64": "arm64"}


class OSSUtilInstall(BaseInstall):
    def __init__(self, version="2.1.2", force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.base_url = "https://gosspublic.alicdn.com/ossutil/v2"
        self.install_path = "~/opt/bin/"
        self.force = force

    def is_installed(self) -> bool:
        if check_command("ossutil version", "ossutil"):
            return True
        install_path_expanded = os.path.expanduser(self.install_path)
        ossutil_path = os.path.join(install_path_expanded, "ossutil")
        if os.path.exists(ossutil_path) and check_command(
            f"{ossutil_path} version", "ossutil"
        ):
            return True
        return False

    def _download_and_install(self, os_name: str, arch_suffix: str) -> bool:
        filename = f"ossutil-{self.version}-{os_name}-{arch_suffix}.zip"
        download_url = f"{self.base_url}/{self.version}/{filename}"
        folder_name = f"ossutil-{self.version}-{os_name}-{arch_suffix}"

        logger.info(f"开始下载 ossutil {self.version} for {os_name} {arch_suffix}")
        for cmd in [
            f"mkdir -p {self.install_path}",
            f"curl -o {filename} {download_url}",
            f"unzip {filename}",
            f"cd {folder_name} && chmod 755 ossutil && mv ossutil {self.install_path}/",
            f"cd .. && rm -rf {filename} {folder_name}",
        ]:
            run_shell(cmd)

        logger.success(f"成功安装 ossutil {self.version} 到 {self.install_path}")
        return True

    def _resolve_arch(self, arch_map: dict) -> str | None:
        arch = platform.machine().lower()
        suffix = arch_map.get(arch)
        if not suffix:
            logger.error(f"不支持的架构: {arch}")
        return suffix

    def install_macos(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            arch_suffix = self._resolve_arch(ARCH_MAP_MAC)
            if not arch_suffix:
                return False
            return self._download_and_install("mac", arch_suffix)
        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_linux(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            arch = platform.machine().lower()
            arch_suffix = ARCH_MAP_LINUX.get(arch)
            if not arch_suffix and arch.startswith("arm"):
                arch_suffix = "arm"
            if not arch_suffix:
                logger.error(f"不支持的架构: {arch}")
                return False
            return self._download_and_install("linux", arch_suffix)
        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_windows(self, *args, **kwargs) -> bool:
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            arch_suffix = self._resolve_arch(ARCH_MAP_GENERIC)
            if not arch_suffix:
                return False

            filename = f"ossutil-{self.version}-windows-{arch_suffix}.zip"
            download_url = f"{self.base_url}/{self.version}/{filename}"
            install_dir = os.path.expanduser(self.install_path)
            folder_name = f"ossutil-{self.version}-windows-{arch_suffix}"

            logger.info(f"开始下载 ossutil {self.version} for Windows {arch_suffix}")
            os.makedirs(install_dir, exist_ok=True)

            for cmd in [
                f'powershell -Command "Invoke-WebRequest -Uri {download_url} -OutFile {filename}"',
                f'powershell -Command "Expand-Archive -Path {filename} -DestinationPath . -Force"',
                f'powershell -Command "Move-Item {folder_name}\\ossutil.exe {install_dir}\\ossutil.exe"',
                f'powershell -Command "Remove-Item {filename}"',
                f'powershell -Command "Remove-Item {folder_name} -Recurse"',
            ]:
                run_shell(cmd)

            logger.success(f"成功安装 ossutil {self.version} 到 {install_dir}")
            logger.info(f"请手动将 {install_dir} 添加到系统环境变量 PATH 中")
            return True
        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            logger.info(f"Windows安装失败，请手动下载: {self.base_url}/{self.version}/")
            return False
