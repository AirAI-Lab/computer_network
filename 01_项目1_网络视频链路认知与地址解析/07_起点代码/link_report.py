from __future__ import annotations

import argparse
from pathlib import Path

from media_info import probe
from url_parser import parse_url


def generate(url: str, media_path: Path, output: Path) -> None:
    # TODO: Parse the URL, probe the media, and write a Markdown report.
    # The report must state what the evidence proves and what it does not prove.
    raise NotImplementedError("complete generate")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--media", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("evidence/link_report.md"))
    args = parser.parse_args()
    generate(args.url, args.media, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
