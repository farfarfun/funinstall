"""funinstall CLI 入口模块，注册所有子命令组。"""

import typer

from .install import install_app

app = typer.Typer(help="funinstall — 快速安装常用开发工具的命令行工具")
app.add_typer(install_app, name="install", help="安装开发工具（go、nodejs、brew 等）")


def funinstall():
    """CLI 主入口函数，由 pyproject.toml [project.scripts] 调用。"""
    app()
