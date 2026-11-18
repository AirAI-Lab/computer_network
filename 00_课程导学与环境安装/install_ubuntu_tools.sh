#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# 项目0：Ubuntu WSL2基础工具安装脚本
# 运行层：Ubuntu WSL2，不在Windows PowerShell中运行。
# 运行目录：
#   cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
# 运行命令：
#   bash install_ubuntu_tools.sh
# ============================================================

# set -e：任一命令失败立即停止，避免“前一步没装好，后一步继续跑”。
# set -u：使用未定义变量时报错，方便发现脚本路径写错。
# set -o pipefail：管道中任意命令失败都算失败，不让错误被最后一个命令掩盖。
set -euo pipefail

COURSE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> 1/5 更新Ubuntu软件源"
echo "    当前目录：${COURSE_DIR}"
echo "    这一步会刷新可用软件包列表，输出较多属正常现象。"
sudo apt-get update

echo "==> 2/5 安装课程基础工具"
echo "    ca-certificates：让HTTPS下载能校验证书。"
echo "    curl：下载Docker官方源和GPG密钥。"
echo "    ffmpeg/ffprobe：推流、拉流、读取媒体信息。"
echo "    git：拉取代码和保存课程作业。"
echo "    jq：在命令行中读取JSON结果。"
echo "    netcat-openbsd：提供nc，用于检查TCP端口。"
echo "    python3/pip/venv：运行课程Python脚本。"
sudo apt-get install -y \
  ca-certificates \
  curl \
  ffmpeg \
  git \
  jq \
  netcat-openbsd \
  python3 \
  python3-pip \
  python3-venv

echo "==> 3/5 创建课程专用Python虚拟环境"
echo "    位置：${COURSE_DIR}/.venv"
echo "    作用：课程Python包与Ubuntu系统Python隔离，卸载或重建不影响系统。"
if [[ ! -d "${COURSE_DIR}/.venv" ]]; then
  python3 -m venv "${COURSE_DIR}/.venv"
fi

echo "==> 4/5 升级虚拟环境中的pip"
"${COURSE_DIR}/.venv/bin/pip" install --upgrade pip

echo "==> 5/5 安装后自检"
echo "    以下每一行都应该有版本号；如果提示command not found，说明安装不完整。"
python3 --version
pip3 --version
ffmpeg -version | head -n 1
ffprobe -version | head -n 1
nc -h 2>&1 | head -n 1 || true
git --version
jq --version
"${COURSE_DIR}/.venv/bin/python" --version

cat <<EOF

Ubuntu基础工具安装完成。

以后进入本目录后，可以先激活虚拟环境：
  source .venv/bin/activate

不激活虚拟环境也可以运行环境验收：
  .venv/bin/python environment_check.py --help

下一步：
  bash install_docker_engine_ubuntu.sh

EOF
