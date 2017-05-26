#!/bin/bash

BUTTON_PIN=6

gpio mode $BUTTON_PIN input

while true; do
  STATUS=`gpio read $BUTTON_PIN`

  if [ "$STATUS" == "0" ]; then
    sudo shutdown -h now
  fi

  sleep 1
done
