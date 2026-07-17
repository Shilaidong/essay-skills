#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
bash "$SCRIPT_DIR/../../sn-image-base/scripts/setup.sh"
echo "sn-infographic ready (depends on sn-image-base)."
