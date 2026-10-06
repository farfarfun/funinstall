"""v2rayA 代理客户端安装模块。

支持 Linux（apt 包管理器）和 macOS（Homebrew）两个平台。
- Linux 参考: https://v2raya.org/docs/prologue/installation/debian/
- macOS 参考: https://v2raya.org/docs/prologue/installation/macos/
"""

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from farlog import getLogger

from .utils import ensure_command_succeeds

logger = getLogger("funinstall")


class V2RayAInstall(BaseInstall):
    """v2rayA 安装器，支持 macOS 和 Linux(Debian/Ubuntu) 平台。

    Args:
        version: 指定安装版本（预留参数，当前未使用）。
        lasted: 是否安装最新版本（预留参数，当前未使用）。
        update: 是否更新已有版本（预留参数，当前未使用）。
    """

    def __init__(
        self,
        version: str | None = None,
        lasted: bool = False,
        update: bool = False,
        *args: object,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.version = version
        self.lasted = lasted
        self.update = update

    def install_macos(self, *args: object, **kwargs: object) -> bool:
        """通过 Homebrew 在 macOS 上安装 v2rayA 并启动服务。"""
        logger.info("开始在 macOS 上安装 v2rayA")
        logger.info("添加 v2rayA 的 Homebrew Tap")
        command = "brew tap v2raya/v2raya"
        ensure_command_succeeds(run_shell(command), command)
        logger.info("通过 brew 安装 v2rayA")
        command = "brew install v2raya/v2raya/v2raya"
        ensure_command_succeeds(run_shell(command), command)
        logger.info("启动 v2rayA 服务")
        command = "brew services start v2raya"
        ensure_command_succeeds(run_shell(command), command)
        logger.success("成功在 macOS 上安装 v2rayA")
        return True

    def install_linux(self, *args: object, **kwargs: object) -> bool:
        """通过 apt 在 Debian/Ubuntu 上安装 v2rayA 并配置开机自启动。"""
        logger.info("开始在 Linux 上安装 v2rayA")
        logger.info("添加 v2rayA 的 GPG 公钥和 APT 源")
        commands = [
            "wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/keyrings/v2raya.asc",
            'echo "deb [signed-by=/etc/apt/keyrings/v2raya.asc] https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list',
        ]
        for command in commands:
            ensure_command_succeeds(run_shell(command), command)
        logger.info("更新 APT 索引")
        command = "sudo apt update"
        ensure_command_succeeds(run_shell(command), command)
        logger.info("安装 v2raya 和 v2ray 核心")
        command = "sudo apt install v2raya v2ray"
        ensure_command_succeeds(run_shell(command), command)
        logger.info("设置 v2rayA 开机自启动")
        command = "sudo systemctl enable v2raya.service"
        ensure_command_succeeds(run_shell(command), command)
        logger.info("启动 v2rayA 服务")
        command = "sudo systemctl start v2raya.service"
        ensure_command_succeeds(run_shell(command), command)
        logger.success("成功在 Linux 上安装 v2rayA")
        return True
