#!/bin/bash
echo -n "Enter FLASK_ENV(dev, prod, test): "
read text
export FLASK_ENV="$text"
echo "$FLASK_ENV"
