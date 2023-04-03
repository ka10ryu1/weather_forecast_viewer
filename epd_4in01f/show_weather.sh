#!/bin/bash
GIT_DIR=/opt/weather_forecast_viewer/
python3 $GIT_DIR/epd_4in01f_main.py \
  --api_key $GIT_DIR/weather_config.json \
  --symbol  $GIT_DIR/symbol \
  --zip 270-2241 \
  --dark
