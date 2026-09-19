# lsof -i tcp:8765
# kill -9 58055
# jupyter-labextension update --all

c = get_config()
c.FileContentsManager.root_dir = "./"
c.InteractiveShell.ast_node_interactivity = "all"
# 每次
c.InteractiveShellApp.exec_lines = [
    "import pandas as pd",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
]

c.IPKernelApp.matplotlib = "inline"
c.NotebookApp.enable_mathjax = True

# “*”代表非本机都可以访问
c.LabApp.ip = "*"
# c.ServerApp.ip = False

# c.ConnectionFileMixin.ip = '172.19.36.38'
c.LabApp.ip = "0.0.0.0"
# c.ServerApp.ip = '0.0.0.0'

# 修改为在启动notebook的时候不启动浏览器
c.LabApp.open_browser = True
# c.ServerApp.open_browser = True

# 指定notebook的服务端口号
c.LabApp.port = 8765
# c.ServerApp.port = 8765

# c.NotebookApp.contents_manager_class = 'notedown.NotedownContentsManager'
# 指定notebook服务的目录（缺省为运行jupyter命令时用户所在的目录，注意此目录不能为隐藏目录）

# 如需设定密码，请勿在此硬编码明文或哈希值：
# 用 `python3 -c "from jupyter_server.auth import passwd; print(passwd())"` 生成哈希，
# 再通过 funsecret 或环境变量注入，不要提交到版本库。
