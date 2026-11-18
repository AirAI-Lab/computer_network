
"""
文件：multi_stream_controller.py
所属项目：项目5 多路流与多协议测试
适用对象：各组课堂补全

目标：启动和停止多路流，拒绝重复app/stream身份，并保存PID清单。
完成标志：start后每路流都有独立PID；stop不会误杀不在清单中的进程。
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
from pathlib import Path
from typing import Any


def load(config_path: Path) -> list[dict[str, Any]]:
    """读取多路流配置。

    TODO-1：补全配置校验
    目标：检查每行必需字段，并识别重复的(app,stream)身份。
    提示：身份必须同时看app和stream，不能只看stream。
    完成标志：两个course/cam_g01会被拒绝。
    """
    raise NotImplementedError("TODO-1：complete load")


def command_for(row: dict[str, Any]) -> list[str]:
    """生成一路推流命令。

    TODO-2：补全command_for
    目标：根据每行server、port、app、stream生成RTMP地址。
    完成标志：两路流只有identity不同，目标地址也随identity变化。
    """
    raise NotImplementedError("TODO-2：complete command_for")


def start(config_path: Path) -> int:
    """启动多路流。

    TODO-3：补全start
    目标：先检查所有输入存在，再逐路启动并写PID清单。
    提示：中途失败时要考虑停止已启动的进程，避免留下半套环境。
    完成标志：logs/multi_stream_pids.json记录每路PID和日志。
    """
    raise NotImplementedError("TODO-3：complete start")


def stop() -> int:
    """停止多路流。

    TODO-4：补全stop
    目标：按PID清单逐个SIGTERM，最后删除清单。
    完成标志：重复stop不报错；不清单外进程。
    """
    raise NotImplementedError("TODO-4：complete stop")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后启动或停止多路流。")
    parser.add_argument("action", choices=["start", "stop"], help="start或stop。")
    parser.add_argument("--config", type=Path, default=Path("multi_stream_config.json"), help="配置文件。")
    args = parser.parse_args()
    try:
        return start(args.config) if args.action == "start" else stop()
    except Exception as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
