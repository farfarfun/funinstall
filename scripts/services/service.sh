#!/usr/bin/env bash
set -euo pipefail

name=${1:?missing service name}
cli=${2:?missing CLI name}
action=${3:-}
runtime_dir="${XDG_STATE_HOME:-$HOME/.local/state}/funinstall/$name/.run"
pid_file="$runtime_dir/service.pid"
log_file="$runtime_dir/service.log"
version_file="$runtime_dir/install-version"

usage() {
  echo "用法: $0 <service> <cli> <install|uninstall|update|start|run|stop|restart|status>" >&2
  exit 2
}

require_cli() {
  command -v "$cli" >/dev/null 2>&1 || {
    echo "未找到已安装的 $cli；请先运行 scripts/setup.sh install-dev 或 install-prod。" >&2
    exit 1
  }
}

write_version() {
  mkdir -p "$runtime_dir"
  local cli_path interpreter
  cli_path=$(command -v "$cli")
  interpreter=$(head -n 1 "$cli_path" | sed 's/^#!//')
  if [[ -n "$interpreter" && -x "$interpreter" ]]; then
    "$interpreter" -c 'from importlib.metadata import version; print(version("funinstall"))' >"$version_file" 2>/dev/null || true
  fi
  [[ -s "$version_file" ]] || printf 'installed CLI: %s\n' "$cli_path" >"$version_file"
}

pid_is_service() {
  [[ -s "$pid_file" ]] || return 1
  local pid
  pid=$(<"$pid_file")
  [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null && ps -p "$pid" -o command= 2>/dev/null | grep -F -- "$cli run" >/dev/null
}

remove_stale_pid() {
  if [[ -e "$pid_file" ]] && ! pid_is_service; then
    echo "$name: 检测到陈旧 PID 文件，已移除。" >&2
    rm -f "$pid_file"
  fi
}

start() {
  require_cli
  mkdir -p "$runtime_dir"
  remove_stale_pid
  if pid_is_service; then
    echo "$name 已在运行 (pid $(<"$pid_file"))"
    return
  fi
  write_version
  nohup "$cli" run >>"$log_file" 2>&1 &
  echo "$!" >"$pid_file"
  echo "$name 已启动 (pid $!)"
}

stop() {
  remove_stale_pid
  if ! pid_is_service; then
    echo "$name 未运行"
    return
  fi
  local pid
  pid=$(<"$pid_file")
  kill "$pid"
  rm -f "$pid_file"
  echo "$name 已停止"
}

status() {
  require_cli
  remove_stale_pid
  if pid_is_service; then
    echo "$name running (pid $(<"$pid_file"))"
  else
    echo "$name stopped"
  fi
  if [[ -f "$version_file" ]]; then
    printf 'installed: '
    head -n 1 "$version_file"
  else
    echo "installed: $(command -v "$cli")"
  fi
  pid_is_service
}

case "$action" in
  install|update)
    require_cli
    "$cli" "$action"
    write_version
    ;;
  uninstall)
    require_cli
    "$cli" uninstall
    rm -f "$version_file"
    ;;
  start) start ;;
  run)
    require_cli
    mkdir -p "$runtime_dir"
    write_version
    exec "$cli" run
    ;;
  stop) stop ;;
  restart) stop; start ;;
  status) status ;;
  *) usage ;;
esac
