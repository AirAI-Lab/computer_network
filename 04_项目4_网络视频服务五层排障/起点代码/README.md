# 项目4｜网络视频服务五层排障

## 五层顺序

```text
1 容器服务：docker ps -a
2 端口映射：docker port zlm_g01
3 网络入口：nc -zv 127.0.0.1 1935
4 媒体列表：getMediaList
5 播放端：VLC或浏览器人工复核
```

## 基本命令

```bash
python3 fault_injector.py --mode service
python3 diagnose.py > evidence/before-recover.txt
python3 fault_injector.py --mode service-recover
python3 diagnose.py > evidence/after-recover.txt
```

## 判断边界

容器Up、端口通、API可达、媒体列表有流，都不能单独代替播放端体验。验收必须保留播放截图。
