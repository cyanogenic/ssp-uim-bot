#!/bin/bash

echo -ne "stoping bot..."
ps -ef | grep "app.py" | grep -v "grep" | awk '{print $2}' | xargs -n1 kill > /dev/null 2>&1
echo "OK"
echo -ne "stoping frp..."
ps -ef | grep "frp" | grep -v "grep" | awk '{print $2}' | xargs -n1 kill > /dev/null 2>&1
echo "OK"