
"""
文件：diagnose.py
所属项目：项目4 网络视频服务五层排障
适用对象：各组课堂补全

目标：按服务、端口映射、网络、媒体、播放五层输出证据。
完成标志：failed层能给出建议；播放层保留manual-review。
"""
from __future__ import annotations

import argparse
import json
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


def run(command: list[str]) -> dict[str, Any]:
    """执行命令并保留输出。

    TODO-1：补全run
    目标：保留ok和output，不让命令异常导致整个诊断中断。
    完成标志：docker不存在时JSON仍能写出失败证据。
    """
    raise NotImplementedError("TODO-1：complete run")


def diagnose(container: str, host: str, port: int, api_secret: str) -> dict[str, Any]:
    """采集五层证据。

    TODO-2：补全diagnose
    目标：分别检查docker ps、docker port、TCP、getMediaList、人工播放。
    提示：不要把五层合成一个布尔值；每层都要有evidence和advice。
    完成标志：断开服务或停止推流后，JSON能指出具体失败层。
    """
    raise NotImplementedError("TODO-2：complete diagnose")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后输出五层排障证据。")
    parser.add_argument("--container", default="zlm_g01", help="容器名。")
    parser.add_argument("--host", default="127.0.0.1", help="RTMP主机。")
    parser.add_argument("--port", type=int, default=1935, help="RTMP端口。")
    parser.add_argument("--secret", default="", help="API密钥。")
    parser.add_argument("--output", type=Path, default=Path("evidence/diagnose.json"), help="JSON输出。")
    args = parser.parse_args()
    result = diagnose(args.container, args.host, args.port, args.secret)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
