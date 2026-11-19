
"""
文件：url_parser.py
所属项目：项目1 网络视频链路认知与地址解析
适用对象：各组课堂补全

目标：把媒体地址拆成协议、主机、端口、应用名和流名。
完成标志：正确解析教师给出的随机地址，并能解释每个字段的工程含义。

零基础语法提示：
    1. raw.strip()去掉字符串首尾空格，返回新字符串，不修改raw。
    2. .lower()把字符串转为小写。
    3. protocol in DEFAULT_PORTS判断字典中是否存在这个协议键。
    4. raw.split("://", 1)按第一个://切一次，返回列表；
       [0]是协议，[1]是剩余地址。
    5. ", ".join(DEFAULT_PORTS)把键拼成可读提示语，不参与网络访问。
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
    提示：
        protocol = raw.strip().lower()
        字符串方法会返回新值，必须赋给protocol。
        再用protocol in DEFAULT_PORTS判断课程是否支持该协议。
        不支持时raise ValueError，错误提示可用", ".join(DEFAULT_PORTS)生成。
        不要把rtmp://整段当成协议。
    输入示例：raw="RTMP"
    完成标志：返回"rtmp"；raw="ftp"时抛出ValueError。
    """
    raise NotImplementedError("TODO-1：complete validate_protocol")


def parse_url(raw: str) -> dict:
    """解析地址五字段。

    TODO-2：补全地址解析
    目标：返回protocol、host、port、app、stream。
    提示：
        先检查raw中是否有"://"。
        raw.split("://", 1)[0]是协议部分，交给validate_protocol。
        urlparse(raw)后，parsed.hostname是主机，parsed.port是端口。
        地址未写端口时parsed.port为None，要从DEFAULT_PORTS取默认端口。
        parsed.path.split("/")会得到路径段，空字符串要过滤。
        path至少要有两段：第一段是app，第二段是stream。
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
