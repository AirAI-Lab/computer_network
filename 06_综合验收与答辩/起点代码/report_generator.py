
"""
文件：report_generator.py
所属项目：综合验收与答辩
适用对象：各组课堂补全

目标：生成功能、证据、故障复盘、AI使用记录、个人贡献和结论边界六部分报告。
完成标志：每个功能至少对应一条可打开的证据。
"""
from __future__ import annotations

import argparse
from pathlib import Path


def generate_report(features: list[str], evidence: list[str], output: Path) -> None:
    """生成报告。

    TODO-1：补全generate_report
    目标：输出功能清单、运行证据、故障复盘、AI使用、个人贡献、结论边界。
    提示：不要生成夸大结论；未验证内容也要写清楚。
    完成标志：acceptance_check.py能识别projectReport项。
    """
    raise NotImplementedError("TODO-1：complete generate_report")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后生成最终报告骨架。")
    parser.add_argument("--features", nargs="*", default=[], help="功能清单。")
    parser.add_argument("--evidence", nargs="*", default=[], help="证据清单。")
    parser.add_argument("--output", type=Path, default=Path("../project_report.md"), help="Markdown输出。")
    args = parser.parse_args()
    generate_report(args.features, args.evidence, args.output)
    print(f"report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
