from __future__ import annotations

import argparse
from pathlib import Path


def build_matrix(config_path: Path, output: Path) -> list[dict]:
    # TODO: Generate RTMP, HTTP-FLV, and HLS rows for every stream identity.
    # Keep result, reason, and time empty for manual playback evidence.
    raise NotImplementedError("complete build_matrix")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("multi_stream_config.json"))
    parser.add_argument("--output", type=Path, default=Path("evidence/protocol_matrix.csv"))
    args = parser.parse_args()
    build_matrix(args.config, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
