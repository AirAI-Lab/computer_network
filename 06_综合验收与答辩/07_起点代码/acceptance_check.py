from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(root: Path, container: str) -> dict:
    # TODO: Check required files, container, RTMP port, and manual playback.
    # Human confirmation must remain manual-review, never automatic passed.
    raise NotImplementedError("complete check")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--container", default="zlm_g01")
    parser.add_argument("--output", type=Path, default=Path("evidence/acceptance.json"))
    args = parser.parse_args()
    result = check(args.root, args.container)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
