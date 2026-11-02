from __future__ import annotations

import argparse
import json
from pathlib import Path


def diagnose(container: str, host: str, port: int, api_secret: str) -> dict:
    # TODO: Collect service, port mapping, network, media list, and manual player review.
    # Do not skip a failed lower layer; record it and explain the conclusion boundary.
    raise NotImplementedError("complete diagnose")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--container", default="zlm_g01")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=1935)
    parser.add_argument("--secret", default="")
    parser.add_argument("--output", type=Path, default=Path("evidence/diagnose.json"))
    args = parser.parse_args()
    result = diagnose(args.container, args.host, args.port, args.secret)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
