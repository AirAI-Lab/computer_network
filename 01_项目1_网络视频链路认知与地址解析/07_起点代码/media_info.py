from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def probe(path: Path) -> dict:
    # TODO: Check that the file exists, run ffprobe, and extract:
    # container, duration, videoCodec, audioCodec, width, and height.
    raise NotImplementedError("complete probe")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    row = probe(args.input)
    print(json.dumps(row, ensure_ascii=False, indent=2))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
