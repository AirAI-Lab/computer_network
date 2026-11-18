# 计算机网络应用

课程代码：0103141201｜教师：文奴

本仓库面向课程学习，包含主课件PDF、项目主线视频课件、原理动画、学生任务卡、起点代码、课程进度表和环境安装指南。任务需要大家自己补全，不提供教师参考代码和标准答案。

## 课程结构

|模块|课时|
|---|---:|
|项目0 课程导学与环境安装|2|
|项目1 网络视频链路认知与地址解析|4|
|项目2 Ubuntu WSL2与Docker部署ZLMediaKit|4|
|项目3 Python与FFmpeg一路流工程化|4|
|项目4 网络视频服务五层排障|4|
|项目5 多路流与多协议测试|4|
|综合验收与答辩|2|

## 第一次上课从哪里开始

1. 阅读 `00_课程导学与环境安装/项目0环境安装与验收指南.docx`。
2. 在Windows PowerShell执行 `wsl -l -v`，确认Ubuntu为WSL2。
3. 在Windows PowerShell执行 `wsl -d Ubuntu`，进入Ubuntu WSL2。
4. 在Ubuntu执行 `/mnt/d/...` 路径；不要在PowerShell执行 `/mnt/d/...`。
5. 按指南完成 Docker Engine 和课程工具安装。
6. 运行项目0 `environment_check.py`，保存JSON与Markdown报告。
7. 用Windows VLC播放 `rtmp://127.0.0.1:1935/course/env_check`，保存画面截图。
8. 按各项目任务卡完成实操和证据归档。

## 环境主线

```text
Windows宿主机
  └── Ubuntu WSL2
        ├── Python、FFmpeg、nc、课程代码
        └── Docker Engine
              └── ZLMediaKit容器
```

课程Python代码在Ubuntu WSL2运行；Windows主要用于文件管理和VLC播放复核。

## 如何运行脚本

- `.sh`安装脚本：在Ubuntu用`bash 脚本名.sh`执行，例如`bash install_ubuntu_tools.sh`。
- `.py`课程脚本：在Ubuntu进入脚本所属项目目录后，用`python3 脚本名.py 参数`执行。
- `url_parser.py`必须带`--url`参数；看到“required: --url”说明Python已运行，只是参数没给。
- VS Code使用WSL远程打开课程目录，集成终端选择Ubuntu，解释器选择`/usr/bin/python3`。
- 详细命令见`脚本运行指南.md`。

## 如何进入Ubuntu和容器

```powershell
# 在Windows PowerShell执行，进入Ubuntu WSL2
wsl -d Ubuntu
```

```bash
# 进入Ubuntu后执行，进入项目0目录
cd '/mnt/d/net-course/计算机网络应用/00_课程导学与环境安装/06_环境安装与自检'
```

```bash
# 容器Up后执行，只进入容器做检查；课程镜像不保证有bash
docker exec -it zlm_g01 sh
pwd
ls
exit
```

`exit` 在容器内执行会回到Ubuntu；在Ubuntu执行会回到PowerShell。课程Python不进入容器运行。

## 目录

- `课件PDF`：7份主课件PDF。
- `视频课件`：7个项目主线视频课件。
- `原理动画`：9条概念与流程动画。
- `00_课程导学与环境安装`：导学、环境指南、自检脚本。
- `01_项目1` 至 `05_项目5`：学生任务卡与起点代码。
- `06_综合验收与答辩`：最终验收任务与起点代码。
- `教学文件`：教学大纲和两个班级进度表。
- `data`：课程共享测试视频。

## 使用提醒

- 起点代码中的TODO需要自己完成，不能直接提交无法解释的AI生成代码。
- 每次实验保存命令、时间、关键输出、异常和恢复复核。
- 端口通不等于有视频流；最终以VLC或浏览器画面为准。
- 欢迎关注空中智能实验室公众号：`qrcode_wechat.jpg`。

## 许可

- 课程文档、课件、视频等教学材料：CC BY-NC 4.0。
- Python、Shell、PowerShell代码：MIT License。
- 详细说明见 `LICENSE`。
