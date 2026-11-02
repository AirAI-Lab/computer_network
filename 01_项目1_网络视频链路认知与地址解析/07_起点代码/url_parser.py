from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse

DEFAULT_PORTS = {"rtmp": 1935, "rtsp": 554, "http": 80}


def validate_protocol(raw: str) -> str:
    # TODO: Remove surrounding spaces, convert to lowercase, and reject unknown protocols.
    raise NotImplementedError("complete validate_protocol")


def parse_url(raw: str) -> dict:
    # TODO: Use urlparse, require a host, and take app/stream from the path.
    # Return protocol, host, port, app, and stream as a dictionary.
    raise NotImplementedError("complete parse_url")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(parse_url(args.url), ensure_ascii=False, indent=2))
        return 0
    except ValueError as error:
        print(json.dumps({"passed": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
