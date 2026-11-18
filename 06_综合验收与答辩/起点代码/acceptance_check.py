
"""
文件：acceptance_check.py
所属项目：综合验收与答辩
适用对象：各组课堂补全

目标：检查必备文件、Python语法、容器、RTMP入口和人工播放复核。
完成标志：failed项为空；播放项保留manual-review并最终由教师现场复核。
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED = [
    "01_项目1_网络视频链路认知与地址解析/07_起点代码/url_parser.py",
    "02_项目2_Ubuntu_WSL2与Docker部署ZLMediaKit/07_起点代码/deploy_check.py",
    "03_项目3_Python与FFmpeg一路流工程化/07_起点代码/stream_controller.py",
    "04_项目4_网络视频服务五层排障/07_起点代码/diagnose.py",
    "05_项目5_多路流与多协议测试/07_起点代码/protocol_matrix.py",
    "06_综合验收与答辩/project_report.md",
]


def check(root: Path, container: str) -> dict[str, Any]:
    """执行综合验收。

    TODO-1：补全check
    目标：检查必备文件、语法、容器、RTMP端口、报告章节和人工播放。
    提示：文件存在不等于语法通过；播放不能自动判passed。
    完成标志：输出rows、failedRows、manualReviewItems。
    """
    raise NotImplementedError("TODO-1：complete check")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后执行综合验收。")
    parser.add_argument("--root", type=Path, default=Path("../.."), help="课程根目录。")
    parser.add_argument("--container", default="zlm_g01", help="容器名。")
    parser.add_argument("--output", type=Path, default=Path("evidence/acceptance.json"), help="JSON输出。")
    args = parser.parse_args()
    result = check(args.root.resolve(), args.container)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
