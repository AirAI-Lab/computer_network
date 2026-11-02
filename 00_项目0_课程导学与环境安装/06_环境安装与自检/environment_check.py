from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(command: list[str], timeout: int = 20) -> dict[str, Any]:
    """Run a command and keep concise output for evidence."""
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        output = (completed.stdout + "\n" + completed.stderr).strip()
        return {
            "ok": completed.returncode == 0,
            "returnCode": completed.returncode,
            "output": output[-2500:],
        }
    except Exception as error:
        return {"ok": False, "returnCode": None, "output": str(error)}


def version_output(command: list[str]) -> dict[str, Any]:
    executable = shutil.which(command[0])
    if not executable:
        return {"ok": False, "path": None, "version": "", "output": "command not found"}
    result = run(command, timeout=15)
    first_lines = [line.strip() for line in result["output"].splitlines() if line.strip()]
    version = first_lines[0] if first_lines else ""
    return {"ok": result["ok"], "path": executable, "version": version, "output": result["output"]}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def check_wsl(args: argparse.Namespace) -> dict[str, Any]:
    proc_version = read_text(Path("/proc/version")).lower()
    distro = os.environ.get("WSL_DISTRO_NAME", "")
    release = read_text(Path("/etc/os-release"))
    ubuntu_match = re.search(r'PRETTY_NAME="([^"]+)"', release)
    is_microsoft = "microsoft" in proc_version or "wsl" in proc_version
    is_ubuntu = "ubuntu" in release.lower()
    return {
        "required": not args.allow_windows_fallback,
        "ok": (is_microsoft and is_ubuntu) or args.allow_windows_fallback,
        "wslDetected": is_microsoft,
        "distribution": distro,
        "linuxVersion": ubuntu_match.group(1) if ubuntu_match else platform.platform(),
        "fallbackAllowed": args.allow_windows_fallback,
    }


def tcp_ok(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except Exception:
        return False


def docker_checks(container: str, image: str | None) -> dict[str, Any]:
    cli = version_output(["docker", "--version"])
    compose = version_output(["docker", "compose", "version"])
    daemon = run(["docker", "info"], timeout=25)
    container_result = run(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Names}}|{{.Status}}|{{.Ports}}"])
    image_result = run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"])
    image_ok = bool(image and image in image_result["output"])
    return {
        "cli": cli,
        "compose": compose,
        "daemon": {"ok": daemon["ok"], "output": daemon["output"][-1200:]},
        "container": {
            "ok": container in container_result["output"] and " up " in container_result["output"].lower(),
            "output": container_result["output"],
        },
        "image": {
            "required": bool(image),
            "ok": image_ok if image else True,
            "output": image_result["output"],
        },
    }


def windows_vlc_check() -> dict[str, Any]:
    candidates = [
        Path("/mnt/c/Program Files/VideoLAN/VLC/vlc.exe"),
        Path("/mnt/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"),
    ]
    found = next((path for path in candidates if path.exists()), None)
    if found:
        result = run([str(found), "--version"], timeout=8)
        return {"ok": True, "path": str(found), "version": result["output"].splitlines()[0] if result["output"] else ""}
    where = run(["powershell.exe", "-NoProfile", "-Command", "Get-Command vlc"], timeout=10)
    return {"ok": where["ok"], "path": "", "version": "", "output": where["output"]}


def ffprobe_media(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"ok": False, "exists": False, "output": f"file not found: {path}"}
    result = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path)
    ], timeout=25)
    media: dict[str, Any] = {"ok": result["ok"], "exists": True, "output": result["output"]}
    if result["ok"]:
        try:
            payload = json.loads(result["output"])
            streams = payload.get("streams", [])
            media["container"] = payload.get("format", {}).get("format_name")
            media["videoCodecs"] = [item.get("codec_name") for item in streams if item.get("codec_type") == "video"]
            media["audioCodecs"] = [item.get("codec_name") for item in streams if item.get("codec_type") == "audio"]
            media["width"] = next((item.get("width") for item in streams if item.get("codec_type") == "video"), None)
            media["height"] = next((item.get("height") for item in streams if item.get("codec_type") == "video"), None)
        except Exception as error:
            media["ok"] = False
            media["parseError"] = str(error)
    return media


def short_push_test(args: argparse.Namespace, data_file: Path) -> dict[str, Any]:
    if args.skip_push:
        return {"required": False, "ok": True, "skipped": True, "reason": "--skip-push"}
    if not data_file.exists():
        return {"required": True, "ok": False, "skipped": False, "reason": "input video not found"}
    target = f"rtmp://{args.rtmp_host}:{args.rtmp_port}/{args.push_app}/{args.push_stream}"
    command = [
        "ffmpeg", "-hide_banner", "-re", "-stream_loop", "-1",
        "-i", str(data_file), "-t", str(args.push_duration),
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
        "-g", "15", "-bf", "0", "-f", "flv", target,
    ]
    result = run(command, timeout=args.push_duration + 25)
    return {
        "required": True,
        "ok": result["ok"],
        "skipped": False,
        "command": " ".join(command),
        "target": target,
        "output": result["output"][-2500:],
    }


def project_files_check(code_dir: Path) -> dict[str, Any]:
    compose = code_dir / "docker-compose.yml"
    env_example = code_dir / ".env.example"
    env = code_dir / ".env"
    return {
        "ok": compose.exists() and env_example.exists() and env.exists(),
        "composeExists": compose.exists(),
        "envExampleExists": env_example.exists(),
        "envExists": env.exists(),
        "path": str(code_dir),
    }


def make_report(result: dict[str, Any]) -> str:
    lines = [
        "# 计算机网络技术基础实训环境自检报告",
        "",
        f"- 检查时间：{result['time']}",
        f"- 主路线：{result['route']}",
        f"- 结论：{'通过' if result['passed'] else '未通过'}",
        "",
        "## 检查结果",
        "",
        "|项目|结果|说明|",
        "|---|---|---|",
    ]
    items: list[tuple[str, bool, str]] = [
        ("WSL Ubuntu", result["wsl"]["ok"], result["wsl"].get("linuxVersion", "")),
        ("Python", result["python"]["ok"], result["python"].get("version", "")),
        ("pip", result["pip"]["ok"], result["pip"].get("version", "")),
        ("FFmpeg", result["ffmpeg"]["ok"], result["ffmpeg"].get("version", "")),
        ("ffprobe", result["ffprobe"]["ok"], result["ffprobe"].get("version", "")),
        ("Docker CLI", result["docker"]["cli"]["ok"], result["docker"]["cli"].get("version", "")),
        ("Docker Compose", result["docker"]["compose"]["ok"], result["docker"]["compose"].get("version", "")),
        ("Docker daemon", result["docker"]["daemon"]["ok"], "docker info 可访问"),
        ("ZLMediaKit容器", result["docker"]["container"]["ok"], result["docker"]["container"].get("output", "")),
        ("RTMP端口", result["port"]["ok"], f"{result['port']['host']}:{result['port']['port']}"),
        ("测试视频", result["media"]["ok"], str(result["media"].get("container", ""))),
        ("项目配置", result["projectFiles"]["ok"], result["projectFiles"]["path"]),
        ("Windows VLC", result["vlc"]["ok"], result["vlc"].get("path", "")),
        ("短时推流", result["push"]["ok"], "已执行" if not result["push"].get("skipped") else "跳过"),
        ("人工播放确认", result["playbackConfirmed"], "VLC已确认画面" if result["playbackConfirmed"] else "待确认"),
    ]
    for name, ok, note in items:
        lines.append(f"|{name}|{'通过' if ok else '未通过'}|{note.replace('|', '/')}|")
    lines.extend(["", "## 边界", ""])
    lines.append("端口通只证明入口可达，不等于视频流存在；播放确认必须由各组在VLC中实际复核。")
    lines.append("短时推流结果只用于环境验收，正式课程仍需重新建立媒体列表和服务状态证据。")
    return "\n".join(lines) + "\n"


def main() -> int:
    package_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Check the course environment in Ubuntu WSL.")
    parser.add_argument(
        "--code-dir",
        type=Path,
        default=package_root / "02_项目2_Ubuntu_WSL2与Docker部署ZLMediaKit" / "06_参考代码",
    )
    parser.add_argument("--data-file", type=Path, default=package_root / "data" / "passage.mp4")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "evidence")
    parser.add_argument("--container", default="zlm_g01")
    parser.add_argument("--image", default="", help="teacher-specified-zlm-image:tag")
    parser.add_argument("--rtmp-host", default="127.0.0.1")
    parser.add_argument("--rtmp-port", type=int, default=1935)
    parser.add_argument("--push-app", default="course")
    parser.add_argument("--push-stream", default="env_check")
    parser.add_argument("--push-duration", type=int, default=5)
    parser.add_argument("--skip-push", action="store_true")
    parser.add_argument("--playback-confirmed", action="store_true")
    parser.add_argument("--allow-windows-fallback", action="store_true")
    args = parser.parse_args()

    code_dir = args.code_dir.resolve()
    data_file = args.data_file.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    result: dict[str, Any] = {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "route": "Windows + Ubuntu WSL2 + Docker" if not args.allow_windows_fallback else "Windows fallback",
        "wsl": check_wsl(args),
        "python": version_output(["python3", "--version"]),
        "pip": version_output(["pip3", "--version"]),
        "ffmpeg": version_output(["ffmpeg", "-version"]),
        "ffprobe": version_output(["ffprobe", "-version"]),
        "docker": docker_checks(args.container, args.image or None),
        "port": {"ok": tcp_ok(args.rtmp_host, args.rtmp_port), "host": args.rtmp_host, "port": args.rtmp_port},
        "media": ffprobe_media(data_file),
        "projectFiles": project_files_check(code_dir),
        "vlc": windows_vlc_check(),
        "playbackConfirmed": bool(args.playback_confirmed),
    }
    result["push"] = short_push_test(args, data_file)

    required = [
        result["wsl"]["ok"],
        result["python"]["ok"],
        result["pip"]["ok"],
        result["ffmpeg"]["ok"],
        result["ffprobe"]["ok"],
        result["docker"]["cli"]["ok"],
        result["docker"]["compose"]["ok"],
        result["docker"]["daemon"]["ok"],
        result["docker"]["container"]["ok"],
        result["port"]["ok"],
        result["media"]["ok"],
        result["projectFiles"]["ok"],
        result["vlc"]["ok"],
        result["push"]["ok"],
        result["playbackConfirmed"],
    ]
    result["passed"] = all(required)

    json_path = output_dir / "environment-check-result.json"
    markdown_path = output_dir / "environment-check-report.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(make_report(result), encoding="utf-8")
    print(json.dumps({
        "passed": result["passed"],
        "json": str(json_path),
        "markdown": str(markdown_path),
    }, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
