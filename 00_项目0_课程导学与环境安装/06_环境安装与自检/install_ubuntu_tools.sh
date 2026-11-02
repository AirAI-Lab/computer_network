#!/usr/bin/env bash
set -euo pipefail

# Install command-line tools needed by this course inside Ubuntu WSL.
sudo apt update
sudo apt install -y \
  ca-certificates \
  curl \
  ffmpeg \
  git \
  jq \
  netcat-openbsd \
  python3 \
  python3-pip \
  python3-venv

# Create an isolated Python environment in the current course directory.
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip

cat <<'EOF'
Ubuntu tools installed.

Next:
1. Install Docker Engine inside Ubuntu: bash install_docker_engine_ubuntu.sh
2. Run: docker --version
3. Run: docker compose version
4. Run: python3 environment_check.py --help
EOF
