#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# 项目0：在Ubuntu WSL2中安装Docker Engine
# 主路线：Windows宿主机 + Ubuntu WSL2 + Ubuntu内Docker Engine。
# 本脚本不安装Docker Desktop；Docker Desktop仅作为备用路线。
# 运行目录：
#   cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
# 运行命令：
#   bash install_docker_engine_ubuntu.sh
# ============================================================

echo "==> 1/8 检查是否在Ubuntu WSL2中"
if ! grep -qi microsoft /proc/version 2>/dev/null; then
  echo "未检测到WSL内核。请先打开Ubuntu终端，再运行本脚本。" >&2
  exit 2
fi
if ! grep -qi ubuntu /etc/os-release; then
  echo "当前WSL发行版不是Ubuntu。课程脚本按Ubuntu编写。" >&2
  exit 2
fi

echo "==> 2/8 安装Docker源依赖"
sudo apt-get update
sudo apt-get install -y ca-certificates curl

echo "==> 3/8 写入Docker官方GPG密钥"
# GPG密钥用于验证软件包确实来自Docker官方源，防止下载源被替换。
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "==> 4/8 添加Docker官方apt源"
. /etc/os-release
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  ${VERSION_CODENAME} stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt-get update

echo "==> 5/8 安装Docker Engine与Compose插件"
# docker-ce：守护进程，负责创建和运行容器。
# docker-ce-cli：docker命令行工具。
# containerd.io：容器运行时。
# docker-buildx-plugin：镜像构建插件。
# docker-compose-plugin：提供docker compose命令，课程部署ZLMediaKit时使用。
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

echo "==> 6/8 把当前用户加入docker组"
# 加入docker组后，普通用户可以直接执行docker命令。
# 组信息在重新打开Ubuntu窗口后生效；当前窗口可用newgrp docker临时生效。
sudo usermod -aG docker "$USER"

echo "==> 7/8 启动Docker服务"
# Ubuntu WSL2可能启用systemd，也可能仍使用传统service命令。
# 两种方式只需要成功执行其中一个。
if command -v systemctl >/dev/null 2>&1 && systemctl is-system-running >/dev/null 2>&1; then
  sudo systemctl enable --now docker
else
  sudo service docker start
fi

echo "==> 8/8 安装自检"
docker --version
docker compose version
if ! docker info >/dev/null 2>&1; then
  cat <<EOF

当前窗口还没有docker组权限，这是常见现象，不代表安装失败。
请先执行：
  newgrp docker
或关闭并重新打开Ubuntu窗口，再执行：
  docker info

EOF
else
  echo "docker info可访问，Docker Engine安装成功。"
  echo "docker ps输出空列表是正常现象，表示当前还没有容器。"
fi

cat <<EOF

Docker Engine安装流程结束。

下一步由教师提供课程镜像文件或镜像加载命令。容器启动将在项目2完成。

EOF
