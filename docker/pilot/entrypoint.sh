#!/usr/bin/env sh
set -eu

if [ -f /run/secrets/codex-auth.json ]; then
  mkdir -p /tmp/.codex
  cp /run/secrets/codex-auth.json /tmp/.codex/auth.json
  chmod 600 /tmp/.codex/auth.json
fi

exec hilbench "$@"
