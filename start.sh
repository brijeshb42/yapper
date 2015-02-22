#!/bin/bash
echo -n "Enter FLASK_ENV(dev, prod, test): "
read text
export FLASK_CONFIG="$text"
echo "$FLASK_CONFIG"
foreman start > logs/access.log
#echo $! > run/server.pid
