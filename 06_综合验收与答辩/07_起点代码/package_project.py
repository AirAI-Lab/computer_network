from __future__ import annotations

import argparse
from pathlib import Path


def package(source: Path, output: Path) -> Path:
    # TODO: Exclude caches, virtual environments, and unnecessary large media.
    # Keep code, configs, reports, logs, screenshots, and JSON/CSV evidence.
    raise NotImplementedError("complete package")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("submission/project-final.zip"))
    args = parser.parse_args()
    print(package(args.source, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
