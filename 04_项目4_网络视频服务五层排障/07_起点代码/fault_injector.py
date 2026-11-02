from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def apply_mode(mode: str, stream_log: Path) -> dict:
    # TODO: Handle service, service-recover, and stream modes separately.
    # Only change one layer at a time so the fault can be used for teaching.
    raise NotImplementedError("complete apply_mode")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["service", "service-recover", "stream"])
    parser.add_argument("--stream-log", type=Path, default=Path("logs/stream.log"))
    parser.add_argument("--output", type=Path, default=Path("evidence/fault_injection.json"))
    args = parser.parse_args()
    row = {"time": datetime.now().isoformat(timespec="seconds"), "mode": args.mode, **apply_mode(args.mode, args.stream_log)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if row["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
