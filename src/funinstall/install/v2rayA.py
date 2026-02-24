"""v2rayA 代理客户端安装模块。

支持 Linux（apt 包管理器）和 macOS（Homebrew）两个平台。
- Linux 参考: https://v2raya.org/docs/prologue/installation/debian/
- macOS 参考: https://v2raya.org/docs/prologue/installation/macos/
"""

from funshell import run_shell
from funserver.servers.base.install import BaseInstall
from nltlog import getLogger

logger = getLogger("funinstall")


class V2RayAInstall(BaseInstall):
    """v2rayA 安装器，支持 macOS 和 Linux(Debian/Ubuntu) 平台。

    Args:
        version: 指定安装版本（预留参数，当前未使用）。
        lasted: 是否安装最新版本（预留参数，当前未使用）。
        update: 是否更新已有版本（预留参数，当前未使用）。
    """

    def __init__(self, version=None, lasted=False, update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.lasted = lasted
        self.update = update

    def install_macos(self, *args, **kwargs) -> bool:
        """通过 Homebrew 在 macOS 上安装 v2rayA 并启动服务。"""
        logger.info("开始在 macOS 上安装 v2rayA")
        logger.info("添加 v2rayA 的 Homebrew Tap")
        run_shell("brew tap v2raya/v2raya")
        logger.info("通过 brew 安装 v2rayA")
        run_shell("brew install v2raya/v2raya/v2raya")
        logger.info("启动 v2rayA 服务")
        run_shell("brew services start v2raya")
        logger.success("成功在 macOS 上安装 v2rayA")
        return True

    def install_linux(self, *args, **kwargs) -> bool:
        """通过 apt 在 Debian/Ubuntu 上安装 v2rayA 并配置开机自启动。"""
        logger.info("开始在 Linux 上安装 v2rayA")
        logger.info("添加 v2rayA 的 GPG 公钥和 APT 源")
        run_shell(
            "wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/keyrings/v2raya.asc"
        )
        run_shell(
            'echo "deb [signed-by=/etc/apt/keyrings/v2raya.asc] https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list'
        )
        logger.info("更新 APT 索引")
        run_shell("sudo apt update")
        logger.info("安装 v2raya 和 v2ray 核心")
        run_shell("sudo apt install v2raya v2ray")
        logger.info("设置 v2rayA 开机自启动")
        run_shell("sudo systemctl enable v2raya.service")
        logger.info("启动 v2rayA 服务")
        run_shell("sudo systemctl start v2raya.service")
        logger.success("成功在 Linux 上安装 v2rayA")
        return True
