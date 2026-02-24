"""阿里云 OSS 命令行工具 (ossutil) 安装模块。

支持 Linux、macOS、Windows 三个平台，自动检测系统架构并下载对应版本。
安装包来源: https://gosspublic.alicdn.com/ossutil/v2
"""

from __future__ import annotations

import os
import platform

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

from .utils import check_command

logger = getLogger("funinstall")

_SKIP_MSG = "ossutil 已安装，跳过安装。如需重新安装，请使用 force=True 参数"

# 平台 -> 架构名称 -> ossutil 架构后缀
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
    """ossutil 安装器，支持 Linux / macOS / Windows 三平台。

    Args:
        version: 指定安装版本，默认 ``2.1.2``。
        force: 为 True 时即使已安装也会重新安装。
    """

    def __init__(self, version="2.1.2", force=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.base_url = "https://gosspublic.alicdn.com/ossutil/v2"
        self.install_path = "~/opt/bin/"
        self.force = force

    def is_installed(self) -> bool:
        """检查 ossutil 是否已安装（同时检查系统 PATH 和自定义安装路径）。"""
        if check_command("ossutil version", "ossutil"):
            return True
        install_path_expanded = os.path.expanduser(self.install_path)
        ossutil_path = os.path.join(install_path_expanded, "ossutil")
        if os.path.exists(ossutil_path) and check_command(
            f"{ossutil_path} version", "ossutil"
        ):
            return True
        logger.debug("ossutil 未安装")
        return False

    def _download_and_install(self, os_name: str, arch_suffix: str) -> bool:
        """下载并解压 ossutil 到安装目录。

        Args:
            os_name: 操作系统标识，如 ``linux``、``mac``。
            arch_suffix: 架构后缀，如 ``amd64``、``arm64``。
        """
        filename = f"ossutil-{self.version}-{os_name}-{arch_suffix}.zip"
        download_url = f"{self.base_url}/{self.version}/{filename}"
        folder_name = f"ossutil-{self.version}-{os_name}-{arch_suffix}"

        logger.info(f"开始下载 ossutil {self.version} for {os_name} {arch_suffix}")
        logger.info(f"下载地址: {download_url}")
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
        """根据架构映射表解析当前系统的架构后缀。

        Args:
            arch_map: 架构名称 -> ossutil 后缀的映射字典。

        Returns:
            匹配的架构后缀，未匹配时返回 None。
        """
        arch = platform.machine().lower()
        suffix = arch_map.get(arch)
        if not suffix:
            logger.error(f"不支持的架构: {arch}")
        else:
            logger.debug(f"检测到架构: {arch} -> {suffix}")
        return suffix

    def install_macos(self, *args, **kwargs) -> bool:
        """在 macOS 上安装 ossutil。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            logger.info("开始在 macOS 上安装 ossutil")
            arch_suffix = self._resolve_arch(ARCH_MAP_MAC)
            if not arch_suffix:
                return False
            return self._download_and_install("mac", arch_suffix)
        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_linux(self, *args, **kwargs) -> bool:
        """在 Linux 上安装 ossutil，额外支持 ARM32 架构。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            logger.info("开始在 Linux 上安装 ossutil")
            arch = platform.machine().lower()
            arch_suffix = ARCH_MAP_LINUX.get(arch)
            # ARM32 架构回退匹配
            if not arch_suffix and arch.startswith("arm"):
                arch_suffix = "arm"
            if not arch_suffix:
                logger.error(f"不支持的架构: {arch}")
                return False
            logger.debug(f"检测到架构: {arch} -> {arch_suffix}")
            return self._download_and_install("linux", arch_suffix)
        except Exception as e:
            logger.error(f"安装 ossutil 失败: {e}")
            return False

    def install_windows(self, *args, **kwargs) -> bool:
        """在 Windows 上安装 ossutil，安装后需手动配置 PATH 环境变量。"""
        if not self.force and self.is_installed():
            logger.info(_SKIP_MSG)
            return True
        try:
            logger.info("开始在 Windows 上安装 ossutil")
            arch_suffix = self._resolve_arch(ARCH_MAP_GENERIC)
            if not arch_suffix:
                return False

            filename = f"ossutil-{self.version}-windows-{arch_suffix}.zip"
            download_url = f"{self.base_url}/{self.version}/{filename}"
            install_dir = os.path.expanduser(self.install_path)
            folder_name = f"ossutil-{self.version}-windows-{arch_suffix}"

            logger.info(f"开始下载 ossutil {self.version} for Windows {arch_suffix}")
            logger.info(f"下载地址: {download_url}")
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
            logger.info(
                f"Windows 安装失败，请手动下载: {self.base_url}/{self.version}/"
            )
            return False
