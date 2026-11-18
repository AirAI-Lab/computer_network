
"""
文件：media_info.py
所属项目：项目1 网络视频链路认知与地址解析
适用对象：各组课堂补全

目标：调用ffprobe读取容器、时长、视频编码、音频编码、宽高。
完成标志：能输出JSON摘要，并说明这些事实不能单独证明网络视频可用。
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe(path: Path) -> dict:
    """读取媒体摘要。

    TODO-1：补全媒体检查
    目标：文件不存在时报错；存在时调用ffprobe并解析JSON。
    提示：命令使用ffprobe -v error -print_format json -show_format -show_streams。
    输入示例：Path('../../data/passage.mp4')
    完成标志：能返回container、duration、videoCodec、audioCodec、width、height。
    """
    raise NotImplementedError("TODO-1：complete probe")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后读取媒体文件事实。")
    parser.add_argument("--input", required=True, type=Path, help="媒体文件路径。")
    parser.add_argument("--json", type=Path, help="可选：保存JSON证据。")
    args = parser.parse_args()
    try:
        row = probe(args.input)
    except Exception as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(row, ensure_ascii=False, indent=2))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
