from __future__ import annotations

import argparse
import json
from pathlib import Path


def check(container: str, ports: list[int]) -> dict:
    # TODO: Check docker ps, docker port, and each TCP port.
    # Keep command output in evidence and distinguish failed from not yet deployed.
    raise NotImplementedError("complete check")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--container", default="zlm_g01")
    parser.add_argument("--ports", default="1935,8080")
    parser.add_argument("--output", type=Path, default=Path("evidence/deploy_check.json"))
    args = parser.parse_args()
    result = check(args.container, [int(x) for x in args.ports.split(",")])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if result.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
