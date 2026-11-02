from __future__ import annotations

import argparse
import json
from pathlib import Path


def start(config_path: Path, input_override: str | None = None, stream_override: str | None = None) -> int:
    # TODO: Read and validate config, apply optional CLI input/stream overrides,
    # build the FFmpeg command, and save pid + log.
    raise NotImplementedError("complete start")


def stop(config_path: Path) -> int:
    # TODO: Read pid file, stop only the process started by this controller, then remove pid file.
    raise NotImplementedError("complete stop")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"])
    parser.add_argument("--config", type=Path, default=Path("stream_config.json"))
    parser.add_argument("--input", dest="input_override")
    parser.add_argument("--stream", dest="stream_override")
    args = parser.parse_args()
    return start(args.config, args.input_override, args.stream_override) if args.action == "start" else stop(args.config)


if __name__ == "__main__":
    raise SystemExit(main())
