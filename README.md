#  ssp-uim-bot
ssp-uim-bot是基于Microsoft Bot FrameWork开发的适用于SSPanel-UIM的bot
#  安装
```
git clone https://github.com/cyanogenic/ssp-uim-bot.git
cd ssp-uim-bot
./bot init
```
初始化完成后根据实际情况修改:

config.py中的APP_ID和APP_PASSWORD(可以从Azure门户中找到)

frp/frpc.ini中的remote_port和local_port(remote_port是实际提供访问的端口,local_port须和config.py中的Port一致)

frp/frpc.ini中的plugin_crt_path和plugin_key_path为ssl证书和秘钥文件的绝对路径

#  使用
## 初始化

## 启动
```
bot start
```
## 停止
```
bot stop
```
## 重启
```
bot restart
```