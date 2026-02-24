"""安装工具模块，提供脚本下载执行和命令检测等通用工具函数。"""

from funshell import run_shell
from nltlog import getLogger

logger = getLogger("funinstall")


def run_script_from_url(
    url: str,
    script_name: str = "funinstall_tmp.sh",
    args: str = "",
    chmod: bool = False,
    sudo: bool = True,
) -> None:
    """从远程 URL 下载 shell 脚本并执行，执行完毕后自动清理临时文件。

    Args:
        url: 脚本的远程下载地址。
        script_name: 下载后保存的本地文件名，默认 ``funinstall_tmp.sh``。
        args: 传给脚本的额外参数字符串。
        chmod: 是否在执行前对脚本添加可执行权限。
        sudo: 是否使用 sudo 执行脚本。
    """
    logger.info(f"正在从 {url} 下载脚本 {script_name}")
    run_shell(f"curl -L -o {script_name} {url}")
    if chmod:
        run_shell(f"chmod +x {script_name}")
    prefix = "sudo " if sudo else ""
    cmd = f"{prefix}bash {script_name}"
    if args:
        cmd += f" {args}"
    logger.info(f"执行脚本: {cmd}")
    run_shell(cmd)
    logger.debug(f"清理临时脚本 {script_name}")
    run_shell(f"rm {script_name}")


def check_command(command: str, name: str) -> bool:
    """通过执行探测命令检查某个命令行工具是否已安装。

    Args:
        command: 用于探测的命令，例如 ``go version``。
        name: 工具的可读名称，用于日志输出。

    Returns:
        已安装返回 True，否则返回 False。
    """
    try:
        run_shell(command)
        logger.info(f"检测到系统中已安装 {name}")
        return True
    except Exception:
        logger.debug(f"未检测到 {name}，探测命令 `{command}` 执行失败")
        return False
