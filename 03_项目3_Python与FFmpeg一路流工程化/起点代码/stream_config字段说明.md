# stream_config.json字段说明

|字段|类型|必填|作用|常见错误|
|---|---|---|---|---|
|input|字符串|是|推流输入媒体路径|路径按运行目录计算，不按文件所在目录计算|
|server|字符串|是|RTMP服务地址，本机实验用127.0.0.1|误写Windows主机局域网IP|
|port|整数|是|RTMP端口，课程默认1935|写成HTTP的8080|
|app|字符串|是|应用名，用于分组|包含斜杠或与其他组混淆|
|stream|字符串|是|流名，一路视频身份|两组同名导致后推覆盖或干扰|
|apiServer|字符串|否|媒体列表接口地址，默认127.0.0.1|与RTMP服务地址混淆|
|apiPort|整数|否|HTTP API端口，默认8080|写成RTMP 1935|
|apiSecret|字符串|否|ZLMediaKit接口密钥，由教师现场提供|把私有密钥提交到公开仓库|
|video|对象|否|编码参数，含codec、preset、tune、gop|追求高画质导致课堂机器卡顿|
|log|字符串|否|FFmpeg日志路径|日志目录不存在导致启动失败|
|pidFile|字符串|否|控制器PID记录|误删后无法安全stop|

## 判断顺序

1. `stream_controller.py start`只说明FFmpeg被启动。
2. `watch_stream.py`看到`app/stream`在线，说明服务端登记了这路流。
3. VLC或浏览器看到画面，才完成播放端复核。
