#!/usr/bin/env bash
# Installs the SysML v2 pilot-implementation Jupyter kernel (used by `sysml_demo.v2.validate`)
# into a micromamba env at $SYSML_ENV (default ~/micromamba/envs/sysml). Idempotent.
set -euo pipefail

ROOT="${MAMBA_ROOT_PREFIX:-$HOME/micromamba}"
BIN="$HOME/bin/micromamba"
ENV_DIR="${SYSML_ENV:-$ROOT/envs/sysml}"

if [ ! -x "$BIN" ]; then
  mkdir -p "$HOME/bin"
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj -C "$HOME" bin/micromamba
fi

export MAMBA_ROOT_PREFIX="$ROOT"
if [ ! -x "$ENV_DIR/bin/python" ]; then
  "$BIN" create -y -p "$ENV_DIR" -c conda-forge "jupyter-sysml-kernel=0.61.0" jupyter_client
fi

echo "SysML v2 kernel ready at $ENV_DIR"
"$ENV_DIR/bin/jupyter" kernelspec list | grep -i sysml
