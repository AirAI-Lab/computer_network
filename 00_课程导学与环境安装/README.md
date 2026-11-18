# 项目0｜环境安装与自检

本目录解决一个问题：正式项目开始前，让大家的电脑具备同一条可复现的实验路线，并能用证据证明环境确实可用。

## 课程主路线

```text
Windows宿主机
  └── Ubuntu WSL2
        ├── Python、FFmpeg、ffprobe、nc、课程代码
        └── Docker Engine
              └── ZLMediaKit容器
```

三层职责如下：

|层|主要用途|本层常做的事|不做的事|
|---|---|---|---|
|Windows|桌面操作和人工播放|打开VLC、查看D盘文件、截图留证|不直接运行课程Python脚本|
|Ubuntu WSL2|命令行实验层|运行Python、FFmpeg、nc、docker命令|不把课程代码复制进容器|
|Docker/ZLMediaKit|流媒体服务|提供RTMP/RTSP/HTTP服务入口|不承担Python教学代码运行|

## 目录对照

Windows资源管理器中：

```text
D:\net-course\计算机网络应用
```

Ubuntu WSL2中访问同一个目录：

```text
/mnt/d/net-course/计算机网络应用
```

## 先确认自己在哪一层

第一次上课最容易混淆的是“Windows PowerShell”和“Ubuntu WSL2”。看提示符可以快速判断：

|当前提示符示例|当前层|能使用的课程路径|下一步|
|---|---|---|---|
|`PS C:\Users\...>`|Windows PowerShell|`D:\net-course\...`|先进入Ubuntu WSL2|
|`用户名@主机名:~$`|Ubuntu WSL2|`/mnt/d/net-course/...`|执行课程安装、Python、FFmpeg、docker命令|
|`/ #`或容器内提示符|ZLMediaKit容器|容器内部路径|只做服务检查，执行`exit`退出|

### 1. 从Windows PowerShell进入Ubuntu WSL2

在Windows PowerShell执行：

```powershell
wsl -l -v
wsl -d Ubuntu
```

`wsl -l -v` 用于确认Ubuntu已经安装且VERSION为2。`wsl -d Ubuntu` 执行后，提示符应从 `PS C:\...>` 变成类似 `用户名@主机名:~$`。

也可以从Windows开始菜单直接打开“Ubuntu”。进入后再执行：

```bash
cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
pwd
ls
```

成功现象：`pwd` 输出 `/mnt/d/net-course/.../06_环境安装与自检`，`ls` 能看到 `environment_check.py`。

如果你在PowerShell中执行 `cd /mnt/d/...`，PowerShell会把它当成 `C:\mnt\d\...`，因此报“找不到路径”。这不是课程目录丢失，而是当前层不对。

### 2. 暂时离开Ubuntu WSL2

在Ubuntu执行：

```bash
exit
```

执行后会回到原来的Windows PowerShell窗口。

## 安装顺序

### 1. 进入Ubuntu并进入项目0自检目录

```bash
cd '/mnt/d/net-course/计算机网络应用'
cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
pwd
```

### 2. 安装Ubuntu基础工具

```bash
bash install_ubuntu_tools.sh
```

成功现象：脚本最后能输出Python、pip、ffmpeg、ffprobe、nc、git、jq的版本信息，并创建 `.venv` 目录。

### 3. 安装Docker Engine

```bash
bash install_docker_engine_ubuntu.sh
```

成功现象：`docker --version`、`docker compose version` 有版本号；重开Ubuntu后 `docker info` 可访问。`docker ps` 显示空列表不是错误，只说明当前还没有容器。

### 4. 准备项目2配置

```bash
cd '/mnt/d/net-course/计算机网络应用/02_项目2_Ubuntu_WSL2与Docker部署ZLMediaKit/07_起点代码'
cp .env.example .env
```

随后按教师现场给出的镜像tag填写 `.env` 中的 `ZLM_IMAGE`。没有获得教师指定值时不要猜测。

### 5. 检查Compose配置并启动容器

```bash
docker compose config --quiet
docker compose up -d
docker ps --filter name=zlm_g01
docker port zlm_g01
```

成功现象：`docker ps` 中能看到 `zlm_g01` 且状态为 `Up`；`docker port` 能看到1935等端口映射。

### 6. 进入容器检查并离开容器

容器为 `Up` 后，可以在Ubuntu中执行：

```bash
docker exec -it zlm_g01 sh
pwd
ls
exit
```

命令含义：

|命令|含义|注意|
|---|---|---|
|`docker exec -it zlm_g01 sh`|进入正在运行的zlm_g01容器|课程镜像不保证有bash，所以用`sh`|
|`pwd`|查看当前在容器内的位置|容器内路径不是Ubuntu的`/mnt/d/...`|
|`ls`|查看容器根目录或当前目录内容|只观察，不修改服务文件|
|`exit`|退出容器，回到Ubuntu WSL2|不会停止容器|

进入容器只用于确认服务进程所在环境。课程Python、FFmpeg推流、任务代码都在Ubuntu WSL2运行，不复制到容器内运行。

### 7. 检查RTMP端口和测试视频

```bash
cd '/mnt/d/net-course/计算机网络应用'
nc -zv 127.0.0.1 1935
ffprobe -v error -show_format -show_streams 'data/passage.mp4'
```

成功现象：`nc` 显示 `succeeded` 或 `open`；`ffprobe` 能输出JSON媒体信息，且streams中包含视频流。

### 8. 运行环境验收

```bash
cd '/mnt/d/net-course/计算机网络应用/00_项目0_课程导学与环境安装/06_环境安装与自检'
python3 environment_check.py
```

脚本会在Ubuntu内执行一次5秒短时推流，并生成：

```text
evidence/environment-check-result.json
evidence/environment-check-report.md
```

### 9. Windows VLC人工复核

在Windows中打开VLC：

```text
媒体 → 打开网络串流 → 网络
```

输入：

```text
rtmp://127.0.0.1:1935/course/env_check
```

看到画面后截图保存到 `evidence`，再执行：

```bash
python3 environment_check.py --skip-push --manual-push-confirmed \
  --playback-confirmed \
  --playback-evidence evidence/vlc-playback.png
```

如果重新执行自动推流，则不需要 `--skip-push`，但仍需要 `--playback-confirmed` 和截图路径。

## 常见问题

### 在PowerShell执行`cd /mnt/d/...`报找不到路径

说明当前还在Windows层。先执行：

```powershell
wsl -d Ubuntu
```

进入Ubuntu后再执行 `/mnt/d/...` 路径。

### 执行`wsl -d Ubuntu`提示找不到发行版

先执行：

```powershell
wsl -l -v
```

如果没有Ubuntu，按项目0指南先安装Ubuntu。如果发行版名称不是Ubuntu，以 `wsl -l -v` 显示的名称为准。

### `docker exec -it zlm_g01 bash`失败

课程容器不保证内置bash。请使用：

```bash
docker exec -it zlm_g01 sh
```

如果容器不是Up状态，先在项目2起点代码目录执行 `docker compose up -d`。

### 提示permission denied while trying to connect to the Docker daemon

这是当前Ubuntu窗口还没有获得docker组权限。先重开Ubuntu窗口；如果必须留在当前窗口，执行：

```bash
newgrp docker
```

### `docker ps` 是空的

空列表不是失败，只说明还没有容器。进入项目2起点代码目录执行：

```bash
docker compose up -d
```

### `docker ps` 显示Up，但VLC没有画面

容器Up只证明服务进程存在，不证明有流在线。依次检查：推流命令是否正常结束、RTMP地址是否正确、VLC是否在推流期间打开。

### 端口检查通过，但没有画面

端口通只证明入口可达。必须有媒体流推入，并由播放端人工复核画面。

## 容器常用命令速查

以下命令都在 **Ubuntu WSL2** 执行，不在Windows PowerShell或容器内部执行。

|命令|作用|成功现象或说明|
|---|---|---|
|`docker ps`|查看当前运行中的容器|能看到`zlm_g01`和`Up`|
|`docker ps -a`|包括已停止的容器|用于查找Exited容器|
|`docker start zlm_g01`|启动已停止的容器|再次`docker ps`看到Up|
|`docker stop zlm_g01`|停止容器|`docker ps`不再显示，`docker ps -a`仍可见|
|`docker restart zlm_g01`|重启容器|服务配置改变后可使用|
|`docker logs --tail 100 zlm_g01`|查看最后100行日志|用于分析启动失败|
|`docker port zlm_g01`|查看端口映射|应看到1935、8080等|
|`docker stats --no-stream`|查看一次容器资源占用|用于多路流负载观察|
|`docker exec -it zlm_g01 sh`|进入容器检查|只检查，不运行课程Python|
|`exit`|从容器回到Ubuntu|容器继续保持运行|

课堂上不要执行 `docker rm`、`docker system prune`、`docker prune` 或删除镜像、删除容器卷的命令；确需重建环境时由教师统一给出命令。

## 验收边界

项目0通过只说明大家具备了进入项目1的环境，不等于完整网络视频系统已经验收。后续项目还会继续区分本地播放、地址结构、服务入口、网络链路和媒体事实。
