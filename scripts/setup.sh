#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "用法: $0 <onehub|newapi|mcphub> <start|run|stop|restart|status|install|uninstall|update>" >&2
  exit 2
}

service=${1:-}
action=${2:-}
case "$service" in
  onehub) cli=funonehub; pid="$HOME/.cache/servers/funonehub/run.pid" ;;
  newapi) cli=funnewapi; pid="$HOME/.cache/servers/funnewapi/run.pid" ;;
  mcphub) cli=funmcphub; pid="$HOME/.cache/servers/funmcphub/run.pid" ;;
  *) usage ;;
esac

case "$action" in
  start|run|stop|restart|install|uninstall|update)
    exec uv run "$cli" "$action"
    ;;
  status)
    if [[ -f "$pid" ]] && kill -0 "$(<"$pid")" 2>/dev/null; then
      echo "$service running (pid $(<"$pid"))"
    else
      echo "$service stopped"
      exit 1
    fi
    ;;
  *) usage ;;
esac
