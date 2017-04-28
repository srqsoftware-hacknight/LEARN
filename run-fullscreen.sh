#!/bin/bash

# a bit hacky wit the sleep + xte stuff
# possibly try kweb, use minimal window manager, etc

sudo -u pi epiphany-browser -a --profile ~/.config http://127.0.0.1:8000/index.html --display=:0 > /dev/null 2>&1 &

sleep 3

xte "key F11" -x:0 &

