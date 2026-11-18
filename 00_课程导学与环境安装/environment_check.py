
"""
文件：environment_check.py
所属项目：项目0 课程导学与环境安装
适用对象：同学环境验收、教师现场复核

一、这个脚本解决什么问题
    它把项目0需要检查的环境证据串成一条链：Ubuntu WSL2、Python、FFmpeg、
    Docker Engine、ZLMediaKit容器、RTMP端口、测试视频、项目配置、短时推流
    和Windows VLC播放复核。脚本不会只看某一个命令“有输出”就判定通过，而是
    保留每一步的命令证据，并明确区分自动检查与人工复核。

二、课程主路线的三层环境
    Windows宿主机
      └── Ubuntu WSL2
            ├── Python、FFmpeg、nc、课程代码
            └── Docker Engine
                  └── ZLMediaKit容器

三、应该在哪里运行
    主路线：Ubuntu WSL2。
    Windows PowerShell只负责打开VLC和查看文件；课程Python脚本不在Windows
    PowerShell中运行，也不复制进ZLMediaKit容器中运行。

四、默认目录
    Windows看到的课程目录：
        D:\net-course\计算机网络应用
    Ubuntu WSL2看到的同一目录：
        /mnt/d/net-course/计算机网络应用

五、常用命令
    cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
    python3 environment_check.py
    python3 environment_check.py --skip-push --manual-push-confirmed
    python3 environment_check.py --playback-confirmed

六、输出文件
    evidence/environment-check-result.json：机器可复核的完整证据。
    evidence/environment-check-report.md：给人看的中文验收报告。

七、状态含义
    passed：本项检查已经通过。
    failed：本项检查失败，需要按处理建议排查。
    manual-review：脚本不能代替人工判断，需要各组在VLC中复核并保存截图。

八、证据边界
    docker ps显示Up，只说明容器进程在运行，不等于有视频流。
    RTMP端口能连通，只说明服务入口可达，不等于流媒体已经可用。
    最终通过必须同时满足：自动检查通过、短时推流成功、VLC人工看到画面。
"""
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


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PROJECT2_NAME = "02_项目2_Ubuntu_WSL2与Docker部署ZLMediaKit"


def run(command: list[str], timeout: int = 20, cwd: Path | None = None) -> dict[str, Any]:
    """执行外部命令，并保留返回码和输出，供报告继续引用。

    参数：
        command: 要执行的命令，每个参数独立成项，避免空格路径被拆开。
        timeout: 最长等待秒数，防止网络或Docker卡住时脚本一直不退出。
        cwd: 命令工作目录，docker compose必须在compose文件所在目录执行。

    返回：
        ok表示返回码是否为0；output合并标准输出和错误输出；returnCode保留
       原始退出码；timedOut表示是否因超时被终止。
    """
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        output = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
        return {
            "ok": completed.returncode == 0,
            "returnCode": completed.returncode,
            "output": output[-4000:],
            "timedOut": False,
        }
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "ok": False,
            "returnCode": None,
            "output": (stdout + "\n" + stderr).strip()[-4000:],
            "timedOut": True,
        }
    except Exception as error:
        return {
            "ok": False,
            "returnCode": None,
            "output": f"无法执行命令 {command[0]}：{error}",
            "timedOut": False,
        }


def status(ok: bool) -> str:
    """把布尔结果转换成报告使用的三种状态。"""
    return "passed" if ok else "failed"


def version_output(command: list[str]) -> dict[str, Any]:
    """检查命令是否存在，并提取第一行版本信息。"""
    executable = shutil.which(command[0])
    if not executable:
        return {
            "status": "failed",
            "path": None,
            "version": "",
            "output": f"未找到命令：{command[0]}",
            "advice": "回到Ubuntu执行项目0工具安装脚本，安装后重新运行本脚本。",
        }
    result = run(command, timeout=15)
    first_line = next((line.strip() for line in result["output"].splitlines() if line.strip()), "")
    return {
        "status": status(result["ok"]),
        "path": executable,
        "version": first_line,
        "output": result["output"],
        "advice": "" if result["ok"] else f"{command[0]}存在但执行失败，请把完整输出发给教师。",
    }


def read_text(path: Path) -> str:
    """读取UTF-8文本；文件不存在或编码异常时返回空字符串。"""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def parse_env_value(env_text: str, key: str) -> str:
    """从.env文本中读取最后一个生效的键值，忽略注释和空行。"""
    value = ""
    for raw_line in env_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        current_key, current_value = line.split("=", 1)
        if current_key.strip() == key:
            value = current_value.strip().strip('"').strip("'")
    return value


def resolve_code_dir(explicit_dir: Path | None) -> dict[str, Any]:
    """定位项目2部署目录，优先使用学生起点代码。

    学生公开包中没有06_参考代码，因此默认顺序必须是07_起点代码在前。
    显式传入--code-dir时只检查该目录，避免脚本悄悄使用另一个目录。
    """
    if explicit_dir:
        candidates = [explicit_dir]
    else:
        candidates = [
            PACKAGE_ROOT / PROJECT2_NAME / "07_起点代码",
            PACKAGE_ROOT / PROJECT2_NAME / "06_参考代码",
        ]
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if (candidate / "docker-compose.yml").is_file():
            return {
                "status": "passed",
                "path": str(candidate),
                "output": f"已找到docker-compose.yml：{candidate / 'docker-compose.yml'}",
                "advice": "",
            }
    return {
        "status": "failed",
        "path": str(explicit_dir.resolve() if explicit_dir else PACKAGE_ROOT / PROJECT2_NAME),
        "output": "未找到docker-compose.yml",
        "advice": (
            "请确认当前目录是 /mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/"
            "06_环境安装与自检，或使用 --code-dir 显式指向项目2/07_起点代码。"
        ),
    }


def check_wsl(allow_windows_fallback: bool) -> dict[str, Any]:
    """确认当前运行层，防止把Windows备用路线误当成课程主路线。"""
    proc_version = read_text(Path("/proc/version")).lower()
    os_release = read_text(Path("/etc/os-release"))
    distro = os.environ.get("WSL_DISTRO_NAME", "")
    pretty = re.search(r'PRETTY_NAME="([^"]+)"', os_release)
    is_microsoft = "microsoft" in proc_version or "wsl" in proc_version
    is_ubuntu = "ubuntu" in os_release.lower()
    ok = (is_microsoft and is_ubuntu) or allow_windows_fallback
    return {
        "status": status(ok),
        "requiredRoute": "Windows + Ubuntu WSL2 + Docker" if not allow_windows_fallback else "Windows fallback",
        "wslDetected": is_microsoft,
        "distribution": distro or (pretty.group(1) if pretty else platform.platform()),
        "output": f"WSL_DISTRO_NAME={distro or '未设置'}；/etc/os-release包含Ubuntu={is_ubuntu}",
        "advice": "" if ok else "请在Ubuntu WSL2终端中运行本脚本，不要在Windows PowerShell中运行。",
    }


def tcp_ok(host: str, port: int) -> bool:
    """用TCP连接检查服务入口是否可达。端口通不等于视频流可用。"""
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except OSError:
        return False


def docker_checks(container: str, image: str, code_dir: Path) -> dict[str, Any]:
    """检查Docker CLI、Compose、daemon、镜像、容器和端口映射。"""
    cli = version_output(["docker", "--version"])
    compose = version_output(["docker", "compose", "version"])
    daemon = run(["docker", "info"], timeout=25)
    container_result = run([
        "docker", "ps", "--filter", f"name=^{container}$", "--format",
        "{{.Names}}|{{.Status}}|{{.Ports}}",
    ])
    container_up = container in container_result["output"] and re.search(r"\|Up\s", container_result["output"]) is not None
    image_result = run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"])
    image_ok = bool(image and image in image_result["output"])
    port_mapping = run(["docker", "port", container])
    compose_config = run(["docker", "compose", "config", "--quiet"], timeout=20, cwd=code_dir)
    container_echo = run(["docker", "exec", container, "sh", "-c", "echo container-shell-ok"])

    return {
        "cli": cli,
        "compose": compose,
        "daemon": {
            "status": status(daemon["ok"]),
            "output": daemon["output"],
            "advice": "" if daemon["ok"] else "Docker daemon未启动或当前用户无权限：重开Ubuntu，或临时执行newgrp docker。",
        },
        "image": {
            "status": status(image_ok),
            "expected": image,
            "output": image_result["output"],
            "advice": "" if image_ok else "教师未下发镜像或镜像未加载。请先向教师确认镜像tag，再执行docker images核对。",
        },
        "container": {
            "status": status(container_up),
            "output": container_result["output"],
            "advice": "" if container_up else "容器不存在或不是Up状态。先在项目2起点代码目录执行docker compose up -d，再执行docker ps。",
        },
        "portMapping": {
            "status": status(port_mapping["ok"] and "1935" in port_mapping["output"]),
            "output": port_mapping["output"],
            "advice": "" if port_mapping["ok"] else "容器未运行时无法查看端口映射。先处理容器状态，再核对compose端口配置。",
        },
        "composeConfig": {
            "status": status(compose_config["ok"]),
            "output": compose_config["output"] or "docker compose config --quiet 无输出，表示语法通过。",
            "advice": "" if compose_config["ok"] else "compose配置无效。检查.env是否存在、ZLM_IMAGE是否为教师指定tag、缩进是否被修改。",
        },
        "containerShell": {
            "status": status(container_echo["ok"]),
            "output": container_echo["output"],
            "advice": "" if container_echo["ok"] else "无法进入容器检查。注意ZLMediaKit容器使用sh，不假设容器内一定有bash。",
        },
    }


def windows_vlc_check(allow_windows_fallback: bool) -> dict[str, Any]:
    """检查Windows侧VLC是否安装。播放确认仍必须人工完成。"""
    candidates = [
        Path("/mnt/c/Program Files/VideoLAN/VLC/vlc.exe"),
        Path("/mnt/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"),
    ]
    found = next((path for path in candidates if path.exists()), None)
    if found:
        return {
            "status": "passed",
            "path": str(found),
            "output": f"找到VLC：{found}",
            "advice": "",
        }
    where = run(["powershell.exe", "-NoProfile", "-Command", "Get-Command vlc"], timeout=10)
    return {
        "status": status(where["ok"]),
        "path": "",
        "output": where["output"],
        "advice": "" if where["ok"] else "在Windows安装VLC后重试。VLC用于最终人工播放复核，不能用端口检查替代。",
    }


def ffprobe_media(path: Path) -> dict[str, Any]:
    """用ffprobe读取测试媒体事实，确认文件不是空文件且包含视频流。"""
    if not path.exists():
        return {
            "status": "failed",
            "exists": False,
            "output": f"测试视频不存在：{path}",
            "advice": "确认课程data目录完整。如果路径不同，请用--data-file显式指定。",
        }
    result = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ], timeout=25)
    media: dict[str, Any] = {
        "status": status(result["ok"]),
        "exists": True,
        "output": result["output"],
        "advice": "" if result["ok"] else "ffprobe读取失败：先单独执行ffprobe命令，确认文件完整、ffmpeg安装成功。",
    }
    if result["ok"]:
        try:
            payload = json.loads(result["output"])
            streams = payload.get("streams", [])
            video_codecs = [item.get("codec_name") for item in streams if item.get("codec_type") == "video"]
            audio_codecs = [item.get("codec_name") for item in streams if item.get("codec_type") == "audio"]
            media.update({
                "container": payload.get("format", {}).get("format_name"),
                "durationSeconds": payload.get("format", {}).get("duration"),
                "videoCodecs": video_codecs,
                "audioCodecs": audio_codecs,
            })
            if not video_codecs:
                media["status"] = "failed"
                media["advice"] = "文件存在但没有视频流，不能作为推流验收素材。"
        except json.JSONDecodeError:
            media["status"] = "failed"
            media["advice"] = "ffprobe输出无法解析为JSON，请保存完整输出并联系教师。"
    return media


def project_files_check(code_dir: Path) -> dict[str, Any]:
    """检查项目2配置文件和.env中的镜像、容器名是否完整。"""
    compose_path = code_dir / "docker-compose.yml"
    env_path = code_dir / ".env"
    missing = [path.name for path in [compose_path, env_path] if not path.is_file()]
    env_text = read_text(env_path)
    image = parse_env_value(env_text, "ZLM_IMAGE")
    container = parse_env_value(env_text, "ZLM_CONTAINER")
    ok = not missing and bool(image) and bool(container)
    details = {
        "compose": str(compose_path),
        "env": str(env_path),
        "ZLM_IMAGE": image,
        "ZLM_CONTAINER": container,
        "missing": missing,
    }
    return {
        "status": status(ok),
        **details,
        "output": json.dumps(details, ensure_ascii=False),
        "advice": "" if ok else (
            "在项目2/07_起点代码中复制.env.example为.env，并由教师现场提供ZLM_IMAGE。"
            "ZLM_CONTAINER保持zlm_g01。"
        ),
    }


def short_push_test(
    data_file: Path,
    host: str,
    port: int,
    app: str,
    stream: str,
    duration: int,
    skip_push: bool,
    manual_push_confirmed: bool,
) -> dict[str, Any]:
    """执行一次短时RTMP推流，作为环境链路的最小自动验证。"""
    url = f"rtmp://{host}:{port}/{app}/{stream}"
    if skip_push:
        return {
            "status": "passed" if manual_push_confirmed else "failed",
            "url": url,
            "mode": "manual" if manual_push_confirmed else "skipped",
            "output": "已声明手动推流并保存证据。" if manual_push_confirmed else "跳过推流且没有手动推流证据。",
            "advice": "" if manual_push_confirmed else "不能跳过推流直接通过。至少执行一次自动或手动短时推流。",
        }
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
        "-re", "-i", str(data_file), "-t", str(duration),
        "-c", "copy", "-f", "flv", url,
    ]
    result = run(command, timeout=max(15, duration + 12))
    return {
        "status": status(result["ok"]),
        "url": url,
        "mode": "automatic",
        "command": " ".join(command),
        "output": result["output"] or "ffmpeg无错误输出，短时推流命令正常结束。",
        "advice": "" if result["ok"] else (
            "推流失败先看三层：容器是否Up、1935端口是否通、RTMP地址是否写成rtmp://127.0.0.1:1935/course/env_check。"
        ),
    }


def playback_check(confirmed: bool, playback_evidence: Path | None) -> dict[str, Any]:
    """人工复核项。脚本只能记录声明，不能代替肉眼确认画面。"""
    evidence_ok = confirmed and (playback_evidence is None or playback_evidence.exists())
    return {
        "status": "passed" if evidence_ok else "manual-review",
        "output": "已在Windows VLC中看到画面。" if evidence_ok else "等待各组在VLC中人工确认画面并保存截图。",
        "evidence": str(playback_evidence) if playback_evidence else "",
        "advice": "" if evidence_ok else "打开VLC → 媒体 → 打开网络串流，输入RTMP地址；看到画面后截图保存到evidence目录。",
    }


def collect_failed(checks: dict[str, Any]) -> list[str]:
    """收集所有failed项，用于判断整体是否还需要人工复核。"""
    failed: list[str] = []

    def walk(value: Any, name: str = "") -> None:
        """递归遍历嵌套检查项，并记录failed状态对应的路径。"""
        if isinstance(value, dict):
            current = name or str(value.get("name", ""))
            if value.get("status") == "failed":
                failed.append(current or "unnamed-check")
            for key, child in value.items():
                if key not in {"output", "advice"}:
                    walk(child, f"{current}/{key}" if current else key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{name}/{index}")

    walk(checks)
    return failed


def classify_result(checks: dict[str, Any]) -> dict[str, Any]:
    """汇总自动项与人工项，failed优先于manual-review。"""
    failed = collect_failed(checks)
    if failed:
        return {"status": "failed", "passed": False, "failedItems": failed, "manualReviewItems": []}
    manual_items = [name for name, value in checks.items() if isinstance(value, dict) and value.get("status") == "manual-review"]
    if manual_items:
        return {"status": "manual-review", "passed": False, "failedItems": [], "manualReviewItems": manual_items}
    return {"status": "passed", "passed": True, "failedItems": [], "manualReviewItems": []}


def make_report(result: dict[str, Any]) -> str:
    """生成中文Markdown报告，方便同学截图和教师快速复核。"""
    status_text = {
        "passed": "通过",
        "failed": "未通过",
        "manual-review": "待人工复核",
    }
    lines = [
        "# 项目0环境验收报告",
        "",
        f"- 生成时间：{result['time']}",
        f"- 运行路线：{result['route']}",
        f"- 总体状态：{status_text[result['summary']['status']]}",
        f"- 结论：{'环境验收通过' if result['summary']['passed'] else '环境尚未完成验收'}",
        "",
        "## 三层环境",
        "",
        "```text",
        "Windows宿主机",
        "  └── Ubuntu WSL2",
        "        ├── Python、FFmpeg、nc、课程代码",
        "        └── Docker Engine",
        "              └── ZLMediaKit容器",
        "```",
        "",
        "## 检查明细",
        "",
        "|检查项|状态|说明|处理建议|",
        "|---|---|---|---|",
    ]
    rows = [
        ("运行层", result["checks"]["wsl"]),
        ("Python", result["checks"]["python"]),
        ("pip", result["checks"]["pip"]),
        ("ffmpeg", result["checks"]["ffmpeg"]),
        ("ffprobe", result["checks"]["ffprobe"]),
        ("Docker CLI", result["checks"]["docker"]["cli"]),
        ("Docker Compose", result["checks"]["docker"]["compose"]),
        ("Docker daemon", result["checks"]["docker"]["daemon"]),
        ("课程镜像", result["checks"]["docker"]["image"]),
        ("ZLMediaKit容器", result["checks"]["docker"]["container"]),
        ("端口映射", result["checks"]["docker"]["portMapping"]),
        ("compose配置", result["checks"]["docker"]["composeConfig"]),
        ("容器进入检查", result["checks"]["docker"]["containerShell"]),
        ("项目配置", result["checks"]["projectFiles"]),
        ("RTMP端口", result["checks"]["port"]),
        ("测试视频", result["checks"]["media"]),
        ("Windows VLC", result["checks"]["vlc"]),
        ("短时推流", result["checks"]["push"]),
        ("人工播放确认", result["checks"]["playback"]),
    ]
    for name, item in rows:
        note = str(item.get("output", item.get("version", ""))).replace("|", "/").replace("\n", " ")
        advice = str(item.get("advice", "")).replace("|", "/").replace("\n", " ")
        state = status_text.get(item.get("status", "failed"), item.get("status", "failed"))
        lines.append(f"|{name}|{state}|{note}|{advice}|")
    lines.extend([
        "",
        "## 证据边界",
        "",
        "- `docker ps`为Up只证明容器进程运行，不证明有视频流。",
        "- `nc`或TCP检查通过只证明端口入口可达，不证明媒体服务可播放。",
        "- `ffmpeg`推流命令正常结束，仍需要在Windows VLC中人工看到画面。",
        "- 通过后请保留JSON报告、Markdown报告和VLC播放截图。",
        "",
    ])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """定义中文CLI参数，帮助第一次上课的同学按需调整。"""
    parser = argparse.ArgumentParser(
        description="项目0环境验收：检查Ubuntu WSL2、Docker、ZLMediaKit、推流和人工播放复核。",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--code-dir", type=Path, default=None, help="项目2compose目录；默认自动查找项目2/07_起点代码。")
    parser.add_argument("--data-file", type=Path, default=PACKAGE_ROOT / "data" / "passage.mp4", help="用于短时推流的测试视频。")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "evidence", help="JSON和Markdown报告输出目录。")
    parser.add_argument("--container", default="zlm_g01", help="ZLMediaKit容器名，与.env保持一致。")
    parser.add_argument("--image", default="", help="课程镜像tag；留空时自动读取.env中的ZLM_IMAGE。")
    parser.add_argument("--rtmp-host", default="127.0.0.1", help="RTMP服务地址。")
    parser.add_argument("--rtmp-port", type=int, default=1935, help="RTMP服务端口。")
    parser.add_argument("--push-app", default="course", help="RTMP应用名。")
    parser.add_argument("--push-stream", default="env_check", help="RTMP流名。")
    parser.add_argument("--push-duration", type=int, default=5, help="自动短时推流秒数。")
    parser.add_argument("--skip-push", action="store_true", help="跳过自动推流；必须配合--manual-push-confirmed。")
    parser.add_argument("--manual-push-confirmed", action="store_true", help="声明已经手动推流并保存证据。")
    parser.add_argument("--playback-confirmed", action="store_true", help="声明已经在Windows VLC中看到画面。")
    parser.add_argument("--playback-evidence", type=Path, default=None, help="VLC播放截图路径；提供后报告会记录并检查文件。")
    parser.add_argument("--allow-windows-fallback", action="store_true", help="允许Windows备用路线；正式课堂默认不使用。")
    return parser


def main() -> int:
    """执行全部检查并写出报告。0通过，2失败，3待人工复核。"""
    args = build_parser().parse_args()
    code_dir_result = resolve_code_dir(args.code_dir)
    if code_dir_result["status"] != "passed":
        print(json.dumps(code_dir_result, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    code_dir = Path(code_dir_result["path"])

    env_text = read_text(code_dir / ".env")
    image = args.image or parse_env_value(env_text, "ZLM_IMAGE")
    container = parse_env_value(env_text, "ZLM_CONTAINER") or args.container

    port_ok = tcp_ok(args.rtmp_host, args.rtmp_port)
    checks: dict[str, Any] = {
        "wsl": check_wsl(args.allow_windows_fallback),
        "python": version_output(["python3", "--version"]),
        "pip": version_output(["pip3", "--version"]),
        "ffmpeg": version_output(["ffmpeg", "-version"]),
        "ffprobe": version_output(["ffprobe", "-version"]),
        "docker": docker_checks(container, image, code_dir),
        "projectFiles": project_files_check(code_dir),
        "port": {
            "status": status(port_ok),
            "host": args.rtmp_host,
            "port": args.rtmp_port,
            "output": "TCP连接成功" if port_ok else "TCP连接失败",
            "advice": "" if port_ok else "先核对docker port；确认1935已映射到本机，再检查容器是否Up。",
        },
        "media": ffprobe_media(args.data_file.resolve()),
        "vlc": windows_vlc_check(args.allow_windows_fallback),
        "push": short_push_test(
            args.data_file.resolve(), args.rtmp_host, args.rtmp_port,
            args.push_app, args.push_stream, args.push_duration,
            args.skip_push, args.manual_push_confirmed,
        ),
        "playback": playback_check(args.playback_confirmed, args.playback_evidence),
    }
    result = {
        "time": dt.datetime.now().isoformat(timespec="seconds"),
        "route": "Windows + Ubuntu WSL2 + Docker" if not args.allow_windows_fallback else "Windows fallback",
        "codeDir": str(code_dir),
        "rtmpUrl": f"rtmp://{args.rtmp_host}:{args.rtmp_port}/{args.push_app}/{args.push_stream}",
        "checks": checks,
    }
    result["summary"] = classify_result(checks)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "environment-check-result.json"
    markdown_path = output_dir / "environment-check-report.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(make_report(result), encoding="utf-8")
    print(json.dumps({
        "summary": result["summary"],
        "json": str(json_path),
        "markdown": str(markdown_path),
    }, ensure_ascii=False, indent=2))
    return {"passed": 0, "failed": 2}.get(result["summary"]["status"], 3)


if __name__ == "__main__":
    raise SystemExit(main())
