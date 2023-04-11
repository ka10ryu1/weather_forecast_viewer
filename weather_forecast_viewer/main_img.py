#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import datetime as dt
from bs4 import BeautifulSoup

from util.config import command
from util.text_request import get_some_txt
from util.img_proc import HTML2Fig, draw_img, get_weather_img, get_concat_v


def forecast(html_doc, symbol, dark_mode=False, row=4, col=1, tmp_row=4, font='IPAexGothic'):

    bg = 'black' if dark_mode else 'azure'
    fg = 'white' if dark_mode else 'dimgrey'

    plt.rcParams['font.family'] = font
    fig = plt.figure(figsize=(4, 2), facecolor=bg)
    plt.subplots_adjust(wspace=0.25, hspace=0.25)

    h2f = HTML2Fig(html_doc, bg, fg, small=True, base=symbol)
    h2f.temp_plot(
        fig.add_subplot(row, col, (2, tmp_row), fc=bg),
        2, gray=True
    )
    plt.tight_layout()
    fig.text(0.02, 0.91, h2f.timestamp, color=fg, fontsize=14)
    fig.canvas.draw()
    return draw_img(fig, h2f.symbols, (6, 40, 18), 38)


def forecast_all(html_doc, symbol, dark_mode=False, row=5, col=1, tmp_row=3, font='IPAexGothic'):

    bg = 'black' if dark_mode else 'azure'
    fg = 'white' if dark_mode else 'dimgrey'

    plt.rcParams['font.family'] = font
    fig = plt.figure(figsize=(16, 9), facecolor=bg)
    plt.subplots_adjust(wspace=0.25, hspace=0.25)

    h2f = HTML2Fig(html_doc, bg, fg, base=symbol)
    h2f.temp_plot(
        fig.add_subplot(row, col, (2, tmp_row), fc=bg),
        1.8
    )
    h2f.other_plot(
        fig.add_subplot(row, col, row - 1, fc=bg),
        h2f.humid, 'blue', (0, 100)
    )
    h2f.other_plot(
        fig.add_subplot(row, col, row, fc=bg),
        h2f.wind, 'green', (0, 12)
    )
    fig.text(0.02, 0.94, h2f.timestamp, color=fg, fontsize=32)

    plt.tight_layout()
    fig.canvas.draw()
    return draw_img(fig, h2f.symbols, (36, 55, 10))


def open_crop_resize(path, crop_size, resize):
    if not path.exists():
        return None

    return Image.open(path).crop(crop_size).resize(resize)


def get_temp(text):
    temp = BeautifulSoup(text, 'html.parser').temperature
    max_temp = str(round(float(temp.get('max')), 1))
    min_temp = str(round(float(temp.get('min')), 1))
    print(f'最高:{max_temp} 最低:{min_temp}')
    return max_temp, min_temp


def draw_footer(img, base, text, height=40, width=640):
    m, d, a = dt.now().strftime('%m %d %a').split()
    c_size = (60, 90, 520, 250)  # Left, Up, Right, Bottom
    r_size = (115, height)
    img_m = open_crop_resize(base / f'{int(m)}m.png', c_size, r_size)
    img_d1 = open_crop_resize(base / f'{d[0]}xd.png', c_size, r_size)
    img_d0 = open_crop_resize(base / f'{d[1]}d.png', c_size, r_size)
    img_a = open_crop_resize(base / f'{a.lower()}.png', c_size, r_size)

    img_w = get_weather_img(text, base).resize((height, height))
    max_temp, min_temp = get_temp(text)

    dst = Image.new('RGBA', (width, height), (0, 0, 0))
    offset = 30
    dst.paste(img_w, (offset, 0), img_w.convert('1'))
    offset = 60
    dist = 105
    dst.paste(img_m, (offset, 0), img_m)
    if img_d1 is not None:
        dst.paste(img_d1, (offset + dist, 0), img_d1)

    dst.paste(img_d0, (offset + dist, 0), img_d0)
    dst.paste(img_a, (offset + dist * 2, 0), img_a)

    draw = ImageDraw.Draw(dst)
    x = 350
    y = 6
    draw_kwgs = {
        'font': ImageFont.truetype('ipaexg.ttf', 24),
        'stroke_width': 2, 'stroke_fill': 'white',
    }
    draw.text((x, y), '最高', 'firebrick', **draw_kwgs)
    draw.text((x + 145, y), '最低', 'royalblue', **draw_kwgs)
    font = ImageFont.truetype('ipaexg.ttf', 32)
    x += 50
    y = 0
    draw.text((x, y), max_temp, 'white', font=font)
    draw.text((x + 145, y), min_temp, 'white', font=font)
    return get_concat_v(img, dst)


def main(args):

    text = get_some_txt(args, ['forecast', 'weather'])
    if text is None:
        return -1

    img = forecast_all(
        text['forecast'], args.symbol, dark_mode=args.dark
    ).resize((640, 360))
    draw_footer(img, args.symbol, text['weather']).save('forecast_all.png')

    img = forecast(
        text['forecast'], args.symbol, dark_mode=args.dark
    ).resize((250, 122))
    img.save('forecast_small.png')
    return 0


if __name__ == '__main__':
    exit(main(command()))
