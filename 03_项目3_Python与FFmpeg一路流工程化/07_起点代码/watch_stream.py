from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


def poll_once(api: str, app: str, stream: str) -> dict:
    # TODO: Request the media-list API and match both app and stream.
    raise NotImplementedError("complete poll_once")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("stream_config.json"))
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--interval", type=int, default=2)
    parser.add_argument("--output", type=Path, default=Path("evidence/stream_watch.csv"))
    args = parser.parse_args()
    # TODO: Loop until duration, write one CSV row per poll, and keep errors as evidence.
    raise NotImplementedError("complete main loop")


if __name__ == "__main__":
    raise SystemExit(main())
