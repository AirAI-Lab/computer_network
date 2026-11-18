
"""
文件：stream_controller.py
所属项目：项目3 Python与FFmpeg一路流工程化
适用对象：各组课堂补全

目标：按配置启动和停止一路FFmpeg推流，并保留PID与日志证据。
完成标志：start后进程可追踪，stop只停止自己启动的进程，不误杀其他FFmpeg。
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    """读取一路流配置。

    TODO-1：补全配置校验
    目标：读取JSON并检查input、server、port、app、stream。
    提示：缺少字段时抛出ValueError，port必须是整数。
    输入示例：stream_config.json。
    完成标志：缺任一必需字段时程序在启动FFmpeg前失败。
    """
    raise NotImplementedError("TODO-1：complete load_config")


def build_command(config: dict[str, Any]) -> list[str]:
    """生成FFmpeg推流命令。

    TODO-2：补全命令构造
    目标：使用-re读取媒体，按配置编码，输出到rtmp://server:port/app/stream。
    提示：输出封装为flv；不要把RTMP地址硬编码。
    完成标志：修改app或stream后，命令中的目标地址同步变化。
    """
    raise NotImplementedError("TODO-2：complete build_command")


def start(config_path: Path, input_override: str | None = None, stream_override: str | None = None) -> int:
    """启动一路流。

    TODO-3：补全start
    目标：应用可选覆盖、检查媒体存在、写日志、保存PID。
    提示：PID文件已存在时应拒绝重复启动。
    完成标志：输出started、pid、log、identity，并能用stop停止。
    """
    raise NotImplementedError("TODO-3：complete start")


def stop(config_path: Path) -> int:
    """停止一路流。

    TODO-4：补全stop
    目标：读取PID，发送SIGTERM，删除PID文件。
    提示：不要用模糊pkill；进程不存在时也要清理过期PID文件。
    完成标志：连续执行两次stop不报错，第二次提示无PID记录。
    """
    raise NotImplementedError("TODO-4：complete stop")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后启动或停止一路FFmpeg推流。")
    parser.add_argument("action", choices=["start", "stop"], help="start启动，stop停止。")
    parser.add_argument("--config", type=Path, default=Path("stream_config.json"), help="配置文件。")
    parser.add_argument("--input", dest="input_override", help="临时覆盖输入媒体。")
    parser.add_argument("--stream", dest="stream_override", help="临时覆盖流名。")
    args = parser.parse_args()
    try:
        return start(args.config, args.input, args.stream_override) if args.action == "start" else stop(args.config)
    except Exception as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
