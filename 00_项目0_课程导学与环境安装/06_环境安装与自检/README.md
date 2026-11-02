# 项目0｜环境安装与自检

目标：在正式项目开始前完成课程主路线环境，并通过一次短时推拉流体验留下问题。

## 主路线

```text
Windows宿主机
└── WSL2 Ubuntu
    ├── Python / FFmpeg / ffprobe / Git / curl / nc
    └── Docker Engine
        └── ZLMediaKit容器
```

## 使用顺序

1. `bash install_ubuntu_tools.sh`
2. `bash install_docker_engine_ubuntu.sh`
3. 加载教师指定ZLMediaKit镜像并启动Compose服务。
4. 执行短时FFmpeg推流，用VLC拉流复核。
5. 运行 `python3 environment_check.py --output-dir evidence`。

## 验收边界

环境自检通过只说明课程环境具备进入项目1的条件，不等于完整视频系统已经验收。项目1将继续区分本地播放、地址结构、服务入口和网络链路证据。
