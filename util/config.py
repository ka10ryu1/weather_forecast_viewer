#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import argparse
from pathlib import Path


def command():
    parser = argparse.ArgumentParser(description='天気表示')

    parser.add_argument(
        '--api_key', default=Path().cwd() / 'weather_config.json',
        help='OpenWeatherMapのAPI key[default: %(default)s]'
    )
    parser.add_argument(
        '--zip_code', default='211-0014',
        help='郵便番号 [default: %(default)s]'
    )
    parser.add_argument(
        '--decode', default='utf-8',
        help='文字コード [default: %(default)s]'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='デバッグモード'
    )
    parser.add_argument(
        '--dark', action='store_true',
        help='ダークモード'
    )

    args = parser.parse_args()
    return args
