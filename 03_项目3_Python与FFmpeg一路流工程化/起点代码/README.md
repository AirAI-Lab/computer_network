# 项目3｜Python与FFmpeg一路流工程化

## 运行目录

```bash
cd '/mnt/d/net-course/计算机网络应用/03_项目3_Python与FFmpeg一路流工程化/07_起点代码'
```

## 基本流程

```bash
# 起点版补全后执行
python3 stream_controller.py start
python3 watch_stream.py --duration 30 --interval 2
python3 stream_controller.py stop
```

## 证据顺序

1. PID与日志证明控制器启动了FFmpeg。
2. 媒体列表CSV证明服务端看到`app/stream`身份。
3. VLC截图证明播放端真实可见。

三者缺一项，都不能写成“完整链路成功”。
