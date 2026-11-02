#!/usr/bin/env bash
set -euo pipefail

# Install Docker Engine inside Ubuntu WSL. This is the course main route;
# Docker Desktop is only the fallback route.
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"

# WSL images may run with or without systemd enabled.
if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
  sudo systemctl enable --now docker
else
  sudo service docker start
fi

cat <<'EOF'
Docker Engine installed.

Important:
1. Close and reopen the Ubuntu window so the docker group takes effect.
2. Verify:
   docker --version
   docker compose version
   docker info
   docker ps
3. If permission is denied during the current session, run: newgrp docker
EOF
