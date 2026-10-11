#!/usr/bin/env bash
set -euo pipefail
exec "$(dirname "${BASH_SOURCE[0]}")/service.sh" newapi funnewapi "${1:-}"
