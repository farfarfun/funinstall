"""安装工具模块，提供脚本下载执行和命令检测等通用工具函数。"""

import shutil
import tempfile
from pathlib import Path

from farlog import getLogger
from funget import download
from funshell import run_shell

logger = getLogger("funinstall")


class ScriptDownloadError(RuntimeError):
    """远程安装脚本下载失败时抛出。"""


def run_script_from_url(
    url: str,
    script_name: str = "funinstall_tmp.sh",
    args: str = "",
    chmod: bool = False,
    sudo: bool = True,
) -> None:
    """从远程 URL 下载 shell 脚本并执行，执行完毕后自动清理临时文件。

    下载统一走组织自有的 ``funget``（带超时、重试与下载字节数校验），
    不在业务代码中直接拼接 ``curl`` 命令；脚本落在独立的临时目录中，
    无论执行成功与否都会清理，避免残留。

    Args:
        url: 脚本的远程下载地址。
        script_name: 下载后保存的本地文件名，默认 ``funinstall_tmp.sh``。
        args: 传给脚本的额外参数字符串。
        chmod: 是否在执行前对脚本添加可执行权限。
        sudo: 是否使用 sudo 执行脚本。

    Raises:
        ScriptDownloadError: 下载失败（网络错误、校验失败等）时抛出。
    """
    tmp_dir = tempfile.mkdtemp(prefix="funinstall_")
    script_path = Path(tmp_dir) / script_name
    try:
        logger.info(f"正在从 {url} 下载脚本 {script_name}")
        if not download(url=url, filepath=str(script_path), overwrite=True):
            raise ScriptDownloadError(f"下载脚本失败: {url}")

        if chmod:
            run_shell(f"chmod +x {script_path}")
        prefix = "sudo " if sudo else ""
        cmd = f"{prefix}bash {script_path}"
        if args:
            cmd += f" {args}"
        logger.info(f"执行脚本: {cmd}")
        exit_code = run_shell(cmd)
        if exit_code != "0":
            raise ScriptDownloadError(f"脚本执行失败（退出码 {exit_code}）: {cmd}")
    finally:
        logger.debug(f"清理临时目录 {tmp_dir}")
        shutil.rmtree(tmp_dir, ignore_errors=True)


def check_command(command: str, name: str) -> bool:
    """通过执行探测命令检查某个命令行工具是否已安装。

    注意：`funshell.run_shell` 在底层子进程失败时并不会抛出异常，而是把
    退出码/错误信息作为字符串返回，因此这里必须显式比对返回值是否为
    ``"0"``，不能依赖 try/except 来判定成败（这是此前的真实 bug：旧实现
    无论命令是否真的存在都会恒为 True，导致 `force=False` 时永远跳过安装）。

    Args:
        command: 用于探测的命令，例如 ``go version``。
        name: 工具的可读名称，用于日志输出。

    Returns:
        已安装返回 True，否则返回 False。
    """
    try:
        result = run_shell(command)
    except Exception as e:
        logger.debug(f"未检测到 {name}，探测命令 `{command}` 执行异常: {e}")
        return False

    if result == "0":
        logger.info(f"检测到系统中已安装 {name}")
        return True
    logger.debug(f"未检测到 {name}，探测命令 `{command}` 退出码: {result}")
    return False
