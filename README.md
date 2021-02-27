# ssp-uim-bot
ssp-uim-bot是基于Microsoft Bot FrameWork开发的适用于SSPanel-UIM的bot
# 安装
```
cp config.py.example config.py
```
根据实际情况修改config.py中的内容，APP_ID和APP_PASSWORD可以从Azure门户中找到

根据实际情况修改frp/frpc.ini中的remote_port和local_port。其中remote_port是实际提供访问的端口、local_port须和config.py中的Port一致
根据实际情况修改frp/frpc.ini中的plugin_crt_path和plugin_key_path为ssl证书和秘钥文件的绝对路径
# 使用
## 启动
```
run.sh
```
## 停止
```
stop.sh
```