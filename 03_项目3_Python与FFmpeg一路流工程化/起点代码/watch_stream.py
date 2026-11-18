
"""
文件：watch_stream.py
所属项目：项目3 Python与FFmpeg一路流工程化
适用对象：各组课堂补全

目标：周期访问媒体列表，同时匹配app和stream，把观测结果写入CSV。
完成标志：CSV保留true/false/error证据，接口一次失败不会中断整个观测。
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen


def load_config(path: Path) -> dict[str, Any]:
    """读取配置。"""
    return json.loads(path.read_text(encoding="utf-8"))


def media_api_url(config: dict[str, Any]) -> str:
    """构造媒体列表地址。

    TODO-1：补全media_api_url
    目标：使用apiServer、apiPort、apiSecret构造getMediaList接口。
    提示：secret需要URL编码，可使用urlencode。
    完成标志：输出地址包含/index/api/getMediaList?secret=。
    """
    raise NotImplementedError("TODO-1：complete media_api_url")


def poll_once(api: str, app: str, stream: str) -> dict[str, Any]:
    """请求并匹配一路流身份。

    TODO-2：补全poll_once
    目标：读取JSON列表，同时匹配app和stream。
    提示：不要只判断列表是否为空，也不要只匹配stream。
    完成标志：app相同但stream不同时online为false。
    """
    raise NotImplementedError("TODO-2：complete poll_once")


def main() -> int:
    """观测主循环。

    TODO-3：补全观测循环
    目标：按duration和interval写CSV，异常记录为error行。
    提示：列建议为time、app、stream、online、detail。
    完成标志：能连续观测60秒并生成完整CSV。
    """
    parser = argparse.ArgumentParser(description="补全后观测媒体列表中的流身份。")
    parser.add_argument("--config", type=Path, default=Path("stream_config.json"), help="配置文件。")
    parser.add_argument("--duration", type=int, default=60, help="观测秒数。")
    parser.add_argument("--interval", type=int, default=2, help="请求间隔秒数。")
    parser.add_argument("--output", type=Path, default=Path("evidence/stream_watch.csv"), help="CSV输出。")
    args = parser.parse_args()
    raise NotImplementedError("TODO-3：complete main loop")


if __name__ == "__main__":
    raise SystemExit(main())
