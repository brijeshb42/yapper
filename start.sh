#!/bin/bash
echo -n "Enter FLASK_ENV(dev, prod, test): "
read text
export FLASK_CONFIG="$text"
echo "$FLASK_CONFIG"
foreman start
#echo $! > run/server.pid
