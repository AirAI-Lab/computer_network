
"""
文件：deploy_check.py
所属项目：项目2 Ubuntu WSL2与Docker部署ZLMediaKit
适用对象：各组课堂补全

目标：把部署证据分成compose配置、容器状态、端口映射和TCP入口四层。
运行目录：项目2/07_起点代码。
完成标志：生成JSON证据，并保留播放端manual-review，不用端口通代替画面确认。
"""
from __future__ import annotations

import argparse
import json
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def run(command: list[str]) -> dict[str, Any]:
    """执行命令并保留输出。

    TODO-1：补全run函数
    目标：调用subprocess.run，保留ok、returnCode和output。
    提示：使用capture_output=True、text=True、encoding="utf-8"、errors="replace"。
    输入示例：["docker","ps","--format","{{.Names}}|{{.Status}}"]
    完成标志：命令返回非0时程序不崩溃，JSON仍保留输出证据。
    """
    raise NotImplementedError("TODO-1：complete run")


def tcp_reachable(host: str, port: int) -> bool:
    """检查一个TCP端口是否能建立连接。

    TODO-2：补全tcp_reachable
    目标：3秒内尝试连接host:port，成功返回True，失败返回False。
    提示：使用socket.create_connection；不要用ping代替TCP端口检查。
    完成标志：服务未启动时为False，服务启动后为True。
    """
    raise NotImplementedError("TODO-2：complete tcp_reachable")


def check(container: str, ports: list[int]) -> dict[str, Any]:
    """生成部署检查结果。

    TODO-3：补全check
    目标：至少采集composeConfig、container、portMapping和每个tcp:端口。
    提示：容器通过不能只看有输出，还要同时满足名称匹配和状态Up。
    输入示例：container="zlm_g01"，ports=[1935,8080]。
    完成标志：失败项有advice；全部自动项通过时overallStatus为passed。
    """
    raise NotImplementedError("TODO-3：complete check")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后检查ZLMediaKit部署证据。")
    parser.add_argument("--container", default="zlm_g01", help="容器名，默认zlm_g01。")
    parser.add_argument("--ports", default="1935,8080", help="待检查端口，英文逗号分隔。")
    parser.add_argument("--output", type=Path, default=Path("evidence/deploy_check.json"), help="JSON输出路径。")
    args = parser.parse_args()
    result = check(args.container, [int(item) for item in args.ports.split(",") if item.strip()])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
