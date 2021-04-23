#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from bs4 import BeautifulSoup

from util import command
from text_request import get_txt

"""
ONNX化はPytorhでできる
ONNXランタイムを試してみる
OAK試してみる話
クリエイター
UNITYのデータセットを試したい
"""


def txt2icon(txt):
    if '01' in txt:  # 快晴
        return chr(int(0x1f31e)) if 'd' in txt else chr(int(0x1f319))
    elif '02' in txt:  # 晴れ
        return chr(int(0x1f324))
    elif '03' in txt or '04' in txt:  # 曇り
        return chr(int(0x1f325))
    elif '09' in txt:  # 霧雨
        return chr(int(0x1f326))
    elif '10' in txt:  # 雨
        return chr(int(0x1f327))
    elif '11' in txt:  # 雷雨
        return chr(int(0x1f329))
    elif '13' in txt:  # 雪
        return chr(int(0x1f328))

    elif '50' in txt:  # 霧
        return chr(int(0x1f32b))

    if 'temp' == txt:
        return chr(int(0x1f321))
    elif 'humid' == txt:
        return chr(int(0x1f322))
    elif 'wind' == txt:
        return chr(int(0x1f32c))

    return txt


def my_weather(args, text):
    if text is None:
        return None

    soup = BeautifulSoup(text, 'html.parser')
    weather = soup.weather.get('icon')
    city = soup.city.get('name')
    if '(' in city:
        city = city.split('(')[0]

    print(f'{txt2icon(weather)} {city}')

    temp = float(soup.temperature.get('value'))
    humidity = int(float(soup.humidity.get('value')))
    hu = soup.humidity.get('unit')
    wind = int(float(soup.speed.get('value')))
    wu = soup.speed.get('unit')
    print(f'{txt2icon("temp")} {temp:.1f}  {txt2icon("humid")} {humidity:.1f}{hu}  {txt2icon("wind")} {wind}{wu}')
    return 0


def main(args):
    if args.debug:
        for i in ('01d', '01n', '02d', '03d', '04d', '09d', '10d', '11d', '13d', '50d', 'temp', 'humid', 'wind', 'o1d'):
            print(txt2icon(i), end='  ')

        print()

    return my_weather(args, get_txt(args, 'weather'))


if __name__ == '__main__':
    exit(main(command()))
