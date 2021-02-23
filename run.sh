#!/bin/bash

WORKSPACE=`dirname $0`
#检查环境
echo "checking python3"
command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 not found,now trying to install it"; sudo apt-get install python3; }
echo "checking python3 venv"
python3 -c "import venv" > /dev/null 2>&1 || { echo >&2 "pyvenv not found,now trying to install it"; sudo apt-get install python3-venv; }

python3 -m venv $WORKSPACE/venv
source $WORKSPACE/venv/bin/activate

pip install -r $WORKSPACE/requirements.txt

#启动
mkdir -p $WORKSPACE/logs
python $WORKSPACE/app.py > $WORKSPACE/logs/app.log 2>&1 &
#反向代理
$WORKSPACE/frp/frps -c $WORKSPACE/frp/frps.ini > /dev/null 2>&1 &
$WORKSPACE/frp/frpc -c $WORKSPACE/frp/frpc.ini > /dev/null 2>&1 &