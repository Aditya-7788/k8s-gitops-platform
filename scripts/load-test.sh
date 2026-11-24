#!/usr/bin/env bash
set -euo pipefail

url="${LOAD_URL:-http://tasks.local:9080/api/load}"
requests="${REQUEST_COUNT:-240}"
concurrency="${CONCURRENCY:-12}"

seq "${requests}" | xargs -P "${concurrency}" -I {} sh -c '
  curl --fail --silent --show-error "$1" >/dev/null
  printf "load request %s completed\n" "$2"
' _ "${url}" {}
