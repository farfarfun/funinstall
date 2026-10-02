# 变更日志

所有关于此项目的重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 为所有安装类添加了 Windows 平台支持
- 统一添加了安装前检查逻辑，避免重复安装
- 新增 OSS 工具（ossutil）安装支持，支持多平台和多架构
- 完善的错误处理和日志记录

### 修复
- 修复了 NodeJS 和 Go 安装类中的语法错误
- 修复了注释中的错误描述
- 统一了代码风格和错误处理模式
- 修复 README 依赖版本与 `pyproject.toml` 不一致、安装示例参数名过期的问题
- 修复 `funjupyter()` CLI 入口调用不存在的 `parse_args()` 导致必然崩溃的问题
- 移除 Jupyter 配置示例中残留的硬编码密码及其哈希值注释
- 声明缺失的 `typer` 直接依赖
- `onehub`/`newapi`/`ossutil`/`run_script_from_url` 统一改用组织自有的 `funget.download` 替代裸 `curl` 下载，具备超时/重试/字节数校验；下载失败时返回 `False`/抛出 `ScriptDownloadError` 而不是静默继续
- `run_script_from_url` 下载的临时脚本改为落在独立临时目录，执行完毕无论成功失败都会清理
- 修复 `check_command` 的真实 bug：`funshell.run_shell` 失败时并不抛异常而是返回错误码字符串，导致旧的 try/except 判断恒为"已安装"，使 Go/NodeJS/ossutil 在 `force=False` 时永远跳过安装
- 为 `brew.py`、`nodejs.py`、`ossutil.py`、`funjupyter/run.py` 中缺失类型注解的公开方法补全类型标注
- 修复 `docs/API.md` 示例代码中的裸 `except:`
- 修正 `docs/DEVELOPMENT_GUIDE.md` 中关于 CHANGELOG 路径的过期说明（已迁移至仓库根目录）

### 变更
- 重构了安装类的基础结构
- 优化了 README 文档，使用表格形式展示支持的工具
- 改进了用户体验和错误提示
- CHANGELOG 由 `docs/CHANGELOG.md` 迁移至仓库根目录
- 因新增依赖 `funget`（仅支持 Python >=3.12），`requires-python` 由 `>=3.10` 上调为 `>=3.12`，与组织内其他依赖 `funget` 的仓库保持一致

## [1.0.54] - 2024-09-22

### 新增
- 基础的安装工具框架
- 支持 Go、NodeJS、Code Server 等工具的安装
- 基于 Typer 的命令行界面

### 废弃
- 部分安装类缺少 Windows 支持
- 缺少安装前检查逻辑
- 代码风格不够统一
