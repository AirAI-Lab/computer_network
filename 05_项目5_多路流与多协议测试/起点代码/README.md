# 项目5｜多路流与多协议测试

## 基本流程

```bash
python3 multi_stream_controller.py start
python3 protocol_matrix.py --output evidence/protocol_matrix.csv
# 按CSV逐项用VLC或浏览器实测，填写result和reason
python3 multi_stream_controller.py stop
```

## 判断边界

PID清单只证明进程启动；协议矩阵只提供待测地址。验收必须逐项记录播放结果、失败原因和截图。
