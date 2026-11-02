from __future__ import annotations

import argparse
from pathlib import Path


def generate_report(features: list[str], evidence: list[str], output: Path) -> None:
    # TODO: Write features, evidence, fault review, AI usage, and personal contribution sections.
    raise NotImplementedError("complete generate_report")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", nargs="*", default=[])
    parser.add_argument("--evidence", nargs="*", default=[])
    parser.add_argument("--output", type=Path, default=Path("project_report.md"))
    args = parser.parse_args()
    generate_report(args.features, args.evidence, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
