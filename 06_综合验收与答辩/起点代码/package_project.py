
"""
文件：package_project.py
所属项目：综合验收与答辩
适用对象：各组课堂补全

目标：打包必要代码、配置、报告和证据，排除缓存、虚拟环境、Git目录和超大媒体。
完成标志：ZIP中能打开project_report.md、起点代码和关键证据。
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDED_PARTS = {"__pycache__", ".venv", "node_modules", ".git", ".pytest_cache", "raw", "temp"}
EXCLUDED_SUFFIXES = {".mp4", ".zip", ".pyc", ".wav", ".mp3"}


def package(source: Path, output: Path) -> Path:
    """创建提交包。

    TODO-1：补全package
    目标：排除缓存、虚拟环境、Git元数据、原始大媒体，保留代码、报告和证据。
    提示：证据目录中的截图可以保留；课程共享mp4不需要重复提交。
    完成标志：ZIP能打开，且不含__pycache__和.venv。
    """
    raise NotImplementedError("TODO-1：complete package")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后打包最终提交。")
    parser.add_argument("--source", type=Path, default=Path("../.."), help="课程根目录。")
    parser.add_argument("--output", type=Path, default=Path("../submission/project-final.zip"), help="ZIP输出。")
    args = parser.parse_args()
    result = package(args.source.resolve(), args.output.resolve())
    print(f"package: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
