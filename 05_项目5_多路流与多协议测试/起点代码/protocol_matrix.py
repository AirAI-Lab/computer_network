
"""
文件：protocol_matrix.py
所属项目：项目5 多路流与多协议测试
适用对象：各组课堂补全

目标：为每路流生成RTMP、HTTP-FLV、HLS地址矩阵，供实测填写。
完成标志：CSV每一行都有协议、身份、地址、播放器、result、reason、time。
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def build_matrix(config_path: Path, output: Path) -> list[dict[str, Any]]:
    """生成协议矩阵。

    TODO-1：补全build_matrix
    目标：每路流生成RTMP、HTTP-FLV、HLS三行。
    提示：HTTP-FLV与HLS使用httpPort，不使用RTMP 1935。
    完成标志：两路流生成6行，且身份互不重复。
    """
    raise NotImplementedError("TODO-1：complete build_matrix")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后生成协议测试矩阵。")
    parser.add_argument("--config", type=Path, default=Path("multi_stream_config.json"), help="多路流配置。")
    parser.add_argument("--output", type=Path, default=Path("evidence/protocol_matrix.csv"), help="CSV输出。")
    args = parser.parse_args()
    try:
        rows = build_matrix(args.config, args.output)
    except Exception as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
