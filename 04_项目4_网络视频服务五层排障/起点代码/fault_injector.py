
"""
文件：fault_injector.py
所属项目：项目4 网络视频服务五层排障
适用对象：各组课堂补全

目标：只制造教师允许的三种可控故障，并保存操作证据。
完成标志：service、service-recover、stream三种模式行为清楚，不使用模糊pkill。
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


def apply_mode(mode: str, stream_log: Path) -> dict[str, Any]:
    """执行故障模式。

    TODO-1：补全apply_mode
    目标：service停止容器，service-recover启动容器，stream停止项目3记录的一路流。
    提示：stream模式应优先读取项目3的logs/stream.pid，不要pkill所有ffmpeg。
    输入示例：mode="stream"，stream_log为日志路径。
    完成标志：每种模式输出ok、output、advice，便于前后对照diagnose.json。
    """
    raise NotImplementedError("TODO-1：complete apply_mode")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后创建或恢复可控故障。")
    parser.add_argument("--mode", required=True, choices=["service", "service-recover", "stream"], help="故障模式。")
    parser.add_argument("--stream-log", type=Path, default=Path("logs/stream.log"), help="推流日志，用于定位线索。")
    parser.add_argument("--output", type=Path, default=Path("evidence/fault_injection.json"), help="JSON输出。")
    args = parser.parse_args()
    row = {"time": datetime.now().isoformat(timespec="seconds"), "mode": args.mode, **apply_mode(args.mode, args.stream_log)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(row, ensure_ascii=False, indent=2))
    return 0 if row["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
