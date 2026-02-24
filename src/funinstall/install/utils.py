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
    """Download a shell script from URL, execute it, and clean up."""
    run_shell(f"curl -L -o {script_name} {url}")
    if chmod:
        run_shell(f"chmod +x {script_name}")
    prefix = "sudo " if sudo else ""
    cmd = f"{prefix}bash {script_name}"
    if args:
        cmd += f" {args}"
    run_shell(cmd)
    run_shell(f"rm {script_name}")


def check_command(command: str, name: str) -> bool:
    """Check if a command-line tool is installed by running a probe command."""
    try:
        run_shell(command)
        logger.info(f"检测到系统中已安装 {name}")
        return True
    except Exception:
        return False
