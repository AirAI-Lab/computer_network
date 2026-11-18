
"""
文件：url_parser.py
所属项目：项目1 网络视频链路认知与地址解析
适用对象：各组课堂补全

目标：把媒体地址拆成协议、主机、端口、应用名和流名。
完成标志：正确解析教师给出的随机地址，并能解释每个字段的工程含义。
"""
from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse


DEFAULT_PORTS = {"rtmp": 1935, "rtsp": 554, "http": 80}


def validate_protocol(raw: str) -> str:
    """校验协议字段。

    TODO-1：补全协议校验
    目标：去掉首尾空格、转小写，只允许rtmp、rtsp、http。
    提示：可使用DEFAULT_PORTS判断，不要把rtmp://整段当成协议。
    输入示例：raw="RTMP"
    完成标志：返回"rtmp"；raw="ftp"时抛出ValueError。
    """
    raise NotImplementedError("TODO-1：complete validate_protocol")


def parse_url(raw: str) -> dict:
    """解析地址五字段。

    TODO-2：补全地址解析
    目标：返回protocol、host、port、app、stream。
    提示：先按://拆协议，再用urlparse取hostname、port和path。
    输入示例：rtmp://127.0.0.1:1935/course/cam_g01
    完成标志：输出端口1935、app为course、stream为cam_g01。
    """
    raise NotImplementedError("TODO-2：complete parse_url")


def main() -> int:
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="补全后解析网络视频地址五字段。")
    parser.add_argument("--url", required=True, help="示例：rtmp://127.0.0.1:1935/course/cam_g01")
    args = parser.parse_args()
    try:
        result = parse_url(args.url)
    except ValueError as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
