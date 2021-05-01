#!/bin/bash

IP_ADDR=$(ip a | grep -A 2 wlan0: | grep "inet 192.168." | sed 's/[\t ]\+/\t/g' | cut -f3)

echo ${IP_ADDR}

python3 /home/pi/Work/weather_forecast_viewer/phat_txt.py -n ${IP_ADDR}
