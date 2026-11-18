
"""
文件：link_report.py
所属项目：项目1 网络视频链路认知与地址解析
适用对象：各组课堂补全

目标：复用url_parser和media_info，生成带证据边界的Markdown报告。
完成标志：报告中能对应五字段和媒体事实，不把本地播放写成网络链路成功。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from media_info import probe
from url_parser import parse_url


def generate(url: str, media_path: Path, output: Path) -> None:
    """生成链路报告。

    TODO-1：补全报告生成
    目标：解析URL、读取媒体信息，并输出URL字段、媒体证据、证据边界三部分。
    提示：先调用parse_url和probe；不要自己手写解析逻辑。
    输入示例：url为rtmp地址，media_path为Path对象。
    完成标志：output生成Markdown，且说明本报告不证明服务在线。
    """
    raise NotImplementedError("TODO-1：complete generate")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后生成项目1链路报告。")
    parser.add_argument("--url", required=True, help="媒体地址。")
    parser.add_argument("--media", required=True, type=Path, help="本地测试媒体。")
    parser.add_argument("--output", type=Path, default=Path("evidence/link_report.md"), help="Markdown输出路径。")
    args = parser.parse_args()
    try:
        generate(args.url, args.media, args.output)
    except Exception as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(f"report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
