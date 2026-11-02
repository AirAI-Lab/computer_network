from __future__ import annotations

import argparse
from pathlib import Path


def start(config_path: Path) -> int:
    # TODO: Reject duplicate app/stream identities, start each FFmpeg process, and save pids.
    raise NotImplementedError("complete start")


def stop() -> int:
    # TODO: Stop only processes listed in the pid manifest, then remove the manifest.
    raise NotImplementedError("complete stop")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"])
    parser.add_argument("--config", type=Path, default=Path("multi_stream_config.json"))
    args = parser.parse_args()
    return start(args.config) if args.action == "start" else stop()


if __name__ == "__main__":
    raise SystemExit(main())
