#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
用法:
  scripts/setup.sh install-dev
  scripts/setup.sh install-prod [version]
  scripts/setup.sh <install|uninstall|update|start|run|stop|restart|status> <onehub|newapi|mcphub>
EOF
  exit 2
}

action=${1:-}
service=${2:-}
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

case "$action" in
  install-dev)
    [[ -z "$service" ]] || usage
    uv tool install --editable "$root" --force
    ;;
  install-prod)
    version=$service
    [[ $# -le 2 ]] || usage
    if [[ -n "$version" ]]; then
      uv tool install "funinstall==$version" --force
    else
      uv tool install funinstall --force
    fi
    ;;
  install|uninstall|update|start|run|stop|restart|status)
    case "$service" in
      onehub|newapi|mcphub)
        exec "$root/scripts/services/$service.sh" "$action"
        ;;
      *) usage ;;
    esac
    ;;
  *) usage ;;
esac
