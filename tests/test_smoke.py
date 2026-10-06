"""funinstall 轻量级冒烟测试套件。

覆盖范围：
  - 顶层包及所有子模块可正常导入。
  - 各安装器类可正常构造，且在调用安装逻辑时通过 mock 隔离所有真实的
    网络请求 / 子进程调用 / 文件系统写操作，避免真正安装或修改宿主系统。
  - CLI 入口（funinstall / funonehub / funmcphub / funnewapi）可正常加载并
    响应 --help。

注意：本仓库（funinstall）本身就是一个“安装脚本合集”，几乎所有类都会执行
真实的 curl/bash/apt/npm/brew 等命令来安装软件，因此这里大量使用
unittest.mock 对 run_shell / run_shell_list / run_script_from_url /
requests.get / os.makedirs 等函数打桩，只验证“调用链路正确”，不触碰真实系统。
"""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

runner = CliRunner()


# ---------------------------------------------------------------------------
# 1. 导入测试：确保包及所有公开子模块可以被正常导入
# ---------------------------------------------------------------------------


def test_import_top_level_package():
    import funinstall

    assert funinstall is not None


def test_import_all_submodules():

    # 确认 install 包对外暴露的公开类均可访问
    from funinstall.install import (
        BrewInstall,
        CodeServerInstall,
        FrpcInstall,
        FunMcpHub,
        FunNewApi,
        FunOneHub,
        GoInstall,
        NodeJSInstall,
        OSSUtilInstall,
        UIFInstall,
        V2RayAInstall,
    )

    for cls in (
        BrewInstall,
        CodeServerInstall,
        FrpcInstall,
        FunMcpHub,
        FunNewApi,
        FunOneHub,
        GoInstall,
        NodeJSInstall,
        OSSUtilInstall,
        UIFInstall,
        V2RayAInstall,
    ):
        assert isinstance(cls, type)


# ---------------------------------------------------------------------------
# 2. CLI 入口冒烟测试：--help 应正常退出，不做真实安装
# ---------------------------------------------------------------------------


def test_funinstall_cli_help():
    from funinstall.command import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "install" in result.output


def test_funinstall_install_subcommand_help():
    from funinstall.command import app

    result = runner.invoke(app, ["install", "--help"])
    assert result.exit_code == 0


def test_funonehub_cli_help():
    from funserver.servers.base import server_parser

    from funinstall.install.onehub import FunOneHub

    with patch("os.makedirs"):
        server = FunOneHub()
    app = server_parser(server)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_funmcphub_cli_help():
    from funserver.servers.base import server_parser

    from funinstall.install.mcphub import FunMcpHub

    with patch("os.makedirs"):
        server = FunMcpHub()
    app = server_parser(server)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_funnewapi_cli_help():
    from funserver.servers.base import server_parser

    from funinstall.install.newapi import FunNewApi

    with patch("os.makedirs"):
        server = FunNewApi()
    app = server_parser(server)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# 3. 安装器类构造测试：仅验证可正常实例化，不触发真实安装
# ---------------------------------------------------------------------------


def test_go_install_construct():
    from funinstall.install.go import GoInstall

    installer = GoInstall(version="1.21.0", force=False)
    assert installer.version == "1.21.0"
    assert installer.force is False


def test_nodejs_install_construct():
    from funinstall.install.nodejs import NodeJSInstall

    installer = NodeJSInstall(version="18.17.0")
    assert installer.version == "18.17.0"
    assert installer.latest is False


def test_frpc_install_construct():
    from funinstall.install.frpc import FrpcInstall

    installer = FrpcInstall()
    assert installer.version == ""


def test_ossutil_install_construct():
    from funinstall.install.ossutil import OSSUtilInstall

    installer = OSSUtilInstall()
    assert installer.version == "2.1.2"
    assert installer.install_path == "~/opt/bin/"


def test_v2raya_install_construct():
    from funinstall.install.v2raya import V2RayAInstall

    installer = V2RayAInstall()
    assert installer.version is None


def test_brew_code_server_uif_construct():
    from funinstall.install.brew import BrewInstall
    from funinstall.install.code_server import CodeServerInstall
    from funinstall.install.uif import UIFInstall

    assert BrewInstall() is not None
    assert CodeServerInstall() is not None
    assert UIFInstall() is not None


def test_server_installers_construct(monkeypatch, tmp_path):
    """FunOneHub/FunMcpHub/FunNewApi 的 __init__ 会创建 ~/.cache/servers/<name> 目录，
    这里把 HOME 重定向到临时目录，避免测试写入真实的用户目录。"""
    monkeypatch.setenv("HOME", str(tmp_path))

    from funinstall.install.mcphub import FunMcpHub
    from funinstall.install.newapi import FunNewApi
    from funinstall.install.onehub import FunOneHub

    onehub = FunOneHub()
    mcphub = FunMcpHub()
    newapi = FunNewApi()

    assert onehub.port == 8801
    assert mcphub.server_name == "funmcphub"
    assert newapi.server_name == "funnewapi"
    # 确认目录确实创建在临时 HOME 下，而不是真实用户目录
    assert str(tmp_path) in onehub.dir_path


# ---------------------------------------------------------------------------
# 4. 安装逻辑冒烟测试：mock 掉所有会真正安装/修改系统的调用
# ---------------------------------------------------------------------------


def test_go_install_linux_skips_when_already_installed():
    """当 is_installed() 为 True 且 force=False 时应直接跳过真实安装步骤。"""
    from funinstall.install.go import GoInstall

    installer = GoInstall()
    with (
        patch.object(installer, "is_installed", return_value=True),
        patch("funinstall.install.go.run_shell", return_value="0") as mock_run_shell,
        patch("funinstall.install.go.run_script_from_url") as mock_run_script,
    ):
        assert installer.install_linux() is True
    mock_run_shell.assert_not_called()
    mock_run_script.assert_not_called()


def test_go_install_windows_unsupported_arch_returns_false():
    from funinstall.install.go import GoInstall

    installer = GoInstall()
    with (
        patch.object(installer, "is_installed", return_value=False),
        patch("funinstall.install.go.platform.machine", return_value="riscv64"),
    ):
        assert installer.install_windows() is False


def test_go_install_windows_mocks_shell():
    """覆盖此前缺失的 Windows 安装路径。"""
    from funinstall.install.go import GoInstall

    installer = GoInstall(version="1.22.0")
    with (
        patch.object(installer, "is_installed", return_value=False),
        patch("funinstall.install.go.platform.machine", return_value="x86_64"),
        patch("funinstall.install.go.run_shell", return_value="0") as mock_run_shell,
    ):
        assert installer.install_windows() is True
    assert mock_run_shell.call_count == 3  # 下载 + 静默安装 + 清理


def test_funinstall_install_cli_nonzero_exit_on_install_failure():
    """安装逻辑抛出异常时，CLI 应以非零退出码结束，而不是静默吞掉错误。"""
    from funinstall.install import install_app

    with patch(
        "funinstall.install.command.GoInstall.install",
        side_effect=RuntimeError("boom"),
    ):
        result = runner.invoke(install_app, ["go"])
    assert result.exit_code != 0


def test_shell_command_failure_raises_instead_of_reporting_success():
    """funshell 以字符串返回退出码时，非零结果必须中断安装流程。"""
    from funinstall.install.utils import ShellCommandError, ensure_command_succeeds

    try:
        ensure_command_succeeds("1", "false")
        raise AssertionError("非零退出码应抛出 ShellCommandError")
    except ShellCommandError as e:
        assert "false" in str(e)


def test_nodejs_install_linux_skips_when_already_installed():
    from funinstall.install.nodejs import NodeJSInstall

    installer = NodeJSInstall()
    with (
        patch.object(installer, "is_installed", return_value=True),
        patch("funinstall.install.nodejs.run_script_from_url") as mock_run_script,
    ):
        assert installer.install_linux() is True
    mock_run_script.assert_not_called()


def test_ossutil_install_linux_skips_when_already_installed():
    from funinstall.install.ossutil import OSSUtilInstall

    installer = OSSUtilInstall()
    with patch.object(installer, "is_installed", return_value=True):
        assert installer.install_linux() is True


def test_ossutil_install_linux_unsupported_arch_returns_false():
    """不支持的 CPU 架构（既不在映射表也不是 arm 前缀）应返回 False，而不是抛异常。"""
    from funinstall.install.ossutil import OSSUtilInstall

    installer = OSSUtilInstall()
    with (
        patch.object(installer, "is_installed", return_value=False),
        patch("funinstall.install.ossutil.platform.machine", return_value="riscv64"),
    ):
        assert installer.install_linux() is False


def test_ossutil_download_failure_returns_false():
    """下载响应异常（如 404/超时）时应返回 False，且不执行解压/安装命令。"""
    from funinstall.install.ossutil import OSSUtilInstall

    installer = OSSUtilInstall()
    with (
        patch.object(installer, "is_installed", return_value=False),
        patch("funinstall.install.ossutil.platform.machine", return_value="x86_64"),
        patch("funinstall.install.ossutil.download", return_value=False),
        patch("funinstall.install.ossutil.run_shell", return_value="0") as mock_run_shell,
    ):
        assert installer.install_linux() is False
    # 仅执行了 mkdir -p，没有继续 unzip/mv/rm
    assert mock_run_shell.call_count == 1


def test_ossutil_install_windows_mocks_shell():
    """覆盖此前缺失的 Windows 安装路径。"""
    from funinstall.install.ossutil import OSSUtilInstall

    installer = OSSUtilInstall()
    with (
        patch.object(installer, "is_installed", return_value=False),
        patch("funinstall.install.ossutil.platform.machine", return_value="x86_64"),
        patch("funinstall.install.ossutil.os.makedirs"),
        patch("funinstall.install.ossutil.run_shell", return_value="0") as mock_run_shell,
    ):
        assert installer.install_windows() is True
    assert mock_run_shell.call_count == 5  # 下载/解压/移动/两次清理


def test_code_server_install_linux_is_mocked():
    """CodeServerInstall 没有 is_installed 短路逻辑，直接 mock 掉脚本执行函数。"""
    from funinstall.install.code_server import CodeServerInstall

    with patch("funinstall.install.code_server.run_script_from_url") as mock_run_script:
        assert CodeServerInstall().install_linux() is True
    mock_run_script.assert_called_once()


def test_frpc_install_linux_is_mocked():
    from funinstall.install.frpc import FrpcInstall

    with patch("funinstall.install.frpc.run_script_from_url") as mock_run_script:
        assert FrpcInstall().install_linux() is True
    mock_run_script.assert_called_once()


def test_uif_install_linux_is_mocked():
    from funinstall.install.uif import UIFInstall

    with (
        patch("funinstall.install.uif.run_script_from_url") as mock_run_script,
        patch("funinstall.install.uif.run_shell", return_value="0") as mock_run_shell,
    ):
        assert UIFInstall().install_linux() is True
    mock_run_script.assert_called_once()
    assert mock_run_shell.call_count == 2  # enable + restart systemd 服务


def test_v2raya_install_linux_is_mocked():
    from funinstall.install.v2raya import V2RayAInstall

    with patch("funinstall.install.v2raya.run_shell", return_value="0") as mock_run_shell:
        assert V2RayAInstall().install_linux() is True
    assert mock_run_shell.called


def test_brew_install_linux_not_supported():
    """Homebrew 不支持 Linux，install_linux 应直接返回 False，无任何副作用。"""
    from funinstall.install.brew import BrewInstall

    assert BrewInstall().install_linux() is False


def test_onehub_get_download_url_mocks_network():
    from funinstall.install.onehub import FunOneHub

    fake_response = MagicMock()
    fake_response.json.return_value = {
        "assets": [{"name": "one-api", "browser_download_url": "http://fake/one-api"}]
    }
    with patch("os.makedirs"):
        onehub = FunOneHub()
    with patch("funinstall.install.onehub.requests.get", return_value=fake_response):
        assets = onehub.get_download_url()
    assert assets == {"one-api": "http://fake/one-api"}


def test_onehub_install_linux_mocks_network_and_shell(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.onehub import FunOneHub

    onehub = FunOneHub()
    with (
        patch.object(
            onehub, "get_download_url", return_value={"one-api": "http://fake/one-api"}
        ),
        patch("funinstall.install.onehub.download", return_value=True) as mock_download,
        patch("funinstall.install.onehub.run_shell_list", return_value="0") as mock_run_shell_list,
    ):
        assert onehub.install_linux() is True
    mock_download.assert_called_once()
    mock_run_shell_list.assert_called_once()


def test_onehub_install_linux_download_failure_returns_false(tmp_path, monkeypatch):
    """下载失败（HTTP 响应异常/网络中断）时应返回 False，且不执行 chmod。"""
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.onehub import FunOneHub

    onehub = FunOneHub()
    with (
        patch.object(
            onehub, "get_download_url", return_value={"one-api": "http://fake/one-api"}
        ),
        patch("funinstall.install.onehub.download", return_value=False),
        patch("funinstall.install.onehub.run_shell_list") as mock_run_shell_list,
    ):
        assert onehub.install_linux() is False
    mock_run_shell_list.assert_not_called()


def test_mcphub_install_linux_mocks_shell(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.mcphub import FunMcpHub

    mcphub = FunMcpHub()
    with patch("funinstall.install.mcphub.run_shell_list", return_value="0") as mock_run_shell_list:
        assert mcphub.install_linux() is True
    mock_run_shell_list.assert_called_once_with(["npm install -g @samanhappy/mcphub"])


def test_newapi_install_linux_mocks_network_and_shell(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.newapi import FunNewApi

    newapi = FunNewApi()
    fake_assets = {"new-api-linux-amd64": "http://fake/new-api"}
    with (
        patch.object(newapi, "get_download_url", return_value=fake_assets),
        patch("funinstall.install.newapi.download", return_value=True) as mock_download,
        patch("funinstall.install.newapi.run_shell_list", return_value="0") as mock_run_shell_list,
    ):
        assert newapi.install_linux() is True
    mock_download.assert_called_once()
    mock_run_shell_list.assert_called_once()


def test_newapi_install_linux_download_failure_returns_false(tmp_path, monkeypatch):
    """下载失败时应返回 False，不应继续执行 chmod。"""
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.newapi import FunNewApi

    newapi = FunNewApi()
    fake_assets = {"new-api-linux-amd64": "http://fake/new-api"}
    with (
        patch.object(newapi, "get_download_url", return_value=fake_assets),
        patch("funinstall.install.newapi.download", return_value=False),
        patch("funinstall.install.newapi.run_shell_list") as mock_run_shell_list,
    ):
        assert newapi.install_linux() is False
    mock_run_shell_list.assert_not_called()


def test_newapi_install_no_matching_asset_raises(tmp_path, monkeypatch):
    """Release 资产里找不到匹配当前平台的产物时，应明确报错而不是静默失败。"""
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.newapi import FunNewApi

    newapi = FunNewApi()
    with patch.object(
        newapi,
        "get_download_url",
        return_value={"new-api-macos-arm64": "http://fake/new-api"},
    ):
        try:
            newapi.install_linux()
            raise AssertionError("应抛出 KeyError：无匹配资产")
        except KeyError:
            pass


def test_utils_run_script_from_url_mocks_shell():
    """utils.run_script_from_url 是所有一键脚本安装逻辑的公共底座，下载统一走
    funget（而不是直接拼接 curl），这里验证正常路径下只执行脚本本身、
    并在成功后清理临时目录。"""
    from funinstall.install.utils import run_script_from_url

    with (
        patch("funinstall.install.utils.download", return_value=True) as mock_download,
        patch("funinstall.install.utils.run_shell", return_value="0") as mock_run_shell,
    ):
        run_script_from_url("http://fake/install.sh", script_name="fake.sh")
    mock_download.assert_called_once()
    assert mock_run_shell.call_count == 1  # 仅执行脚本，下载和清理不再经 run_shell


def test_utils_run_script_from_url_chmod_adds_extra_call():
    """chmod=True 时应额外执行一次 chmod。"""
    from funinstall.install.utils import run_script_from_url

    with (
        patch("funinstall.install.utils.download", return_value=True),
        patch("funinstall.install.utils.run_shell", return_value="0") as mock_run_shell,
    ):
        run_script_from_url("http://fake/install.sh", script_name="fake.sh", chmod=True)
    assert mock_run_shell.call_count == 2  # chmod + 执行脚本


def test_utils_run_script_from_url_download_failure_raises_and_cleans_up():
    """下载失败（网络错误/校验不通过）时应抛出异常，且不应继续执行脚本；
    临时目录也必须被清理，不留下垃圾文件。"""
    import os

    from funinstall.install import utils as utils_module
    from funinstall.install.utils import ScriptDownloadError, run_script_from_url

    captured_dirs = []
    real_mkdtemp = utils_module.tempfile.mkdtemp

    def _tracking_mkdtemp(*args, **kwargs):
        path = real_mkdtemp(*args, **kwargs)
        captured_dirs.append(path)
        return path

    with (
        patch("funinstall.install.utils.download", return_value=False),
        patch("funinstall.install.utils.run_shell") as mock_run_shell,
        patch(
            "funinstall.install.utils.tempfile.mkdtemp", side_effect=_tracking_mkdtemp
        ),
    ):
        try:
            run_script_from_url("http://fake/install.sh", script_name="fake.sh")
            raise AssertionError("应抛出 ScriptDownloadError")
        except ScriptDownloadError:
            pass
    mock_run_shell.assert_not_called()
    assert captured_dirs and not os.path.exists(captured_dirs[0])


def test_utils_run_script_from_url_cleans_up_even_if_script_fails():
    """脚本执行本身失败（非零退出）时，临时目录依然必须被清理。

    注意：`funshell.run_shell` 从不抛异常，失败时只会把退出码作为字符串
    返回（例如 "1"），所以这里用返回值模拟失败，而不是 side_effect 抛异常——
    这正是 check_command 曾经的真实 bug 的根源，见 check_command 的修复。
    """
    import os

    from funinstall.install import utils as utils_module
    from funinstall.install.utils import ScriptDownloadError, run_script_from_url

    captured_dirs = []
    real_mkdtemp = utils_module.tempfile.mkdtemp

    def _tracking_mkdtemp(*args, **kwargs):
        path = real_mkdtemp(*args, **kwargs)
        captured_dirs.append(path)
        return path

    with (
        patch("funinstall.install.utils.download", return_value=True),
        patch("funinstall.install.utils.run_shell", return_value="1"),
        patch(
            "funinstall.install.utils.tempfile.mkdtemp", side_effect=_tracking_mkdtemp
        ),
    ):
        try:
            run_script_from_url("http://fake/install.sh", script_name="fake.sh")
            raise AssertionError("应抛出 ScriptDownloadError")
        except ScriptDownloadError:
            pass
    assert captured_dirs and not os.path.exists(captured_dirs[0])
    assert captured_dirs and not os.path.exists(captured_dirs[0])


def test_utils_check_command_no_real_execution():
    """check_command 探测一个几乎不可能存在的命令，验证异常被正确捕获返回 False，
    且底层依然是通过 mock 的 run_shell，不做真实探测。"""
    from funinstall.install.utils import check_command

    with patch(
        "funinstall.install.utils.run_shell", side_effect=Exception("not found")
    ):
        assert check_command("nonexistent-cmd --version", "nonexistent") is False


# ---------------------------------------------------------------------------
# 5. funjupyter 子模块：未在 [project.scripts] 注册，供 funinstall 内部复用。
#    历史上 funjupyter() 曾调用 typer.Typer 对象上不存在的 parse_args()，必然
#    崩溃；现已改为与 funonehub/funmcphub/funnewapi 一致的 app() 调用方式。
# ---------------------------------------------------------------------------


def test_funjupyter_server_construct(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    from funinstall.install.funjupyter.run import FunJupyter

    server = FunJupyter()
    cmd = server.run_cmd()
    assert "jupyter lab" in cmd


def test_funjupyter_cli_entry_help():
    """funjupyter() 内部构造的 typer app 应能正常响应 --help，不再复现历史上
    调用不存在的 parse_args() 导致的崩溃。"""
    from funserver.servers.base import server_parser

    from funinstall.install.funjupyter.run import FunJupyter

    with patch("os.makedirs"):
        server = FunJupyter()
    app = server_parser(server)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
