# 项目2｜Docker部署ZLMediaKit

## 三层位置

```text
Windows宿主机
  └── Ubuntu WSL2
        └── Docker Engine
              └── ZLMediaKit容器
```

课程Python脚本在Ubuntu WSL2运行；ZLMediaKit容器只提供流媒体服务。

## 准备配置

```bash
cd '/mnt/d/net-course/计算机网络应用/02_项目2_Ubuntu_WSL2与Docker部署ZLMediaKit/07_起点代码'
cp .env.example .env
```

`ZLM_IMAGE`由教师现场指定；未获得指定值前保持为空。`ZLM_CONTAINER`保持`zlm_g01`。

## 启动与复核

```bash
docker compose config --quiet
docker compose up -d
docker ps --filter name=zlm_g01
docker port zlm_g01
python3 deploy_check.py --ports 1935,8080
```

## 结果边界

`deploy_check.py`通过只证明部署入口可用，不证明已有媒体流在线。必须在推流后用VLC或浏览器复核画面并保存截图。
