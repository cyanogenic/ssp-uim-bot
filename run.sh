#!/bin/bash

WORKSPACE=`dirname $0`

# 检查环境
echo -ne "checking python3..."
command -v python3 > /dev/null 2>&1 || { echo >&2 "python3 not found,now trying to install it"; sudo apt-get install python3; }
sudo apt-get install libxml2-dev libxslt1-dev python3-dev zlib1g-dev libevent-dev lxml > /dev/null 2>&1
echo "OK"
echo -ne "checking python3 venv..."
python3 -c "import venv" > /dev/null 2>&1 || { echo >&2 "pyvenv not found,now trying to install it"; sudo apt-get install python3-venv; }
echo "OK"


echo -ne "deploying venv..."
if [ "`$WORKSPACE/venv/bin/python -V | cut -d '.' -f 1`" != "Python 3" ];then
    python3 -m venv $WORKSPACE/venv
fi
source $WORKSPACE/venv/bin/activate
echo "OK"

echo -ne "checking requirements..."
pip install -r $WORKSPACE/requirements.txt -q
echo "OK"

# 启动Bot
mkdir -p $WORKSPACE/logs
python $WORKSPACE/app.py > $WORKSPACE/logs/app.log 2>&1 &
echo "bot started"
# 启动frp
($WORKSPACE/frp/frps -c $WORKSPACE/frp/frps.ini > /dev/null 2>&1 &) && ($WORKSPACE/frp/frpc -c $WORKSPACE/frp/frpc.ini > /dev/null 2>&1 &)
echo "frp started"
