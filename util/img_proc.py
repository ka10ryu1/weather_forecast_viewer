#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path
from datetime import datetime as dt

import numpy as np
from matplotlib import ticker
from matplotlib.patheffects import withStroke
from bs4 import BeautifulSoup


def txt2icon(txt, base, ext='.png'):

    if '01' in txt:    # 快晴
        name = '2600' if 'd' in txt else '2b50'
    elif '02' in txt:  # 晴れ
        name = '1f324' if 'd' in txt else '2b50'
    elif '03' in txt:  # 曇り
        name = '1f325' if 'd' in txt else '2b50'
    elif '04' in txt:  # 曇り
        name = '2601'
    elif '09' in txt:  # 霧雨
        name = '1f326'
    elif '10' in txt:  # 雨
        name = '1f327'
    elif '11' in txt:  # 雷雨
        name = '26c8'
    elif '13' in txt:  # 雪
        name = '2744'
    elif '50' in txt:  # 霧
        name = '1f32b'

    return base / f'{name}{ext}'


def get_weather_img(text, base):
    icon_path = txt2icon(
        BeautifulSoup(text, 'html.parser').weather.get('icon'), base
    )
    return Image.open(icon_path)


class HTML2Fig(object):

    def __init__(self, html_doc, bg, fg, small=False, base=Path.cwd() / 'symbol'):
        self._hour = []
        self._symbols = []
        self._temp = []
        self._humid = []
        self._wind = []
        self._timestamp = None
        self._bg = bg
        self._fg = fg
        self._small = small
        self._base = base
        self.__call__(html_doc)

    @property
    def symbols(self):
        return self._symbols

    @property
    def temp(self):
        return list(map(int, self._temp))

    @property
    def humid(self):
        return list(map(int, self._humid))

    @property
    def wind(self):
        return [round(i, 1) for i in self._wind]

    @property
    def timestamp(self):
        timestamps = self._timestamp.split('-')
        return f'{"/".join(timestamps[:3])} {":".join(timestamps[3:])}'

    def __repr__(self):
        hour = self._hour[-1]
        symbols = self._symbols[-1].as_posix()
        temp = self._temp[-1]
        humid = self._humid[-1]
        wind = self._wind[-1]
        # return f'{hour=:5}, {symbol=:},\t{temp=:5.2f}, {humid=:4.1f}, {wind=:5.2f}'
        return f'h={hour:5}, sym={symbols:},\ttmp{temp:5.2f}, hmd={humid:4.1f}, win={wind:5.2f}'

    def _str(self, soup, tag):
        return soup.get(tag)

    def _float(self, soup, tag):
        return float(self._str(soup, tag))

    def _icon(self, soup, tag):
        return txt2icon(self._str(soup, tag), self._base)

    def __call__(self, html_doc, num=8):
        soup = BeautifulSoup(html_doc, features='html.parser')
        locate = soup.weatherdata.location.find('name').string

        for sfc in soup.forecast.contents[:num]:
            date, time = sfc.get('from').split('T')
            d = int(date.split('-')[2])
            h = int(time.split(':')[0]) + 9
            if self._small:
                h = f'{h if h <= 24 else (h - 24)}'
            else:
                h = f'{d if h <= 24 else (d + 1)}-{h if h <= 24 else (h - 24)}'

            self._hour.append(h)
            self._symbols.append(self._icon(sfc.symbol, 'var'))
            self._temp.append(self._float(sfc.temperature, 'value'))
            self._humid.append(self._float(sfc.humidity, 'value'))
            self._wind.append(self._float(sfc.windspeed, 'mps'))
            print(self.__repr__())

        self._timestamp = f'{locate} {dt.now().strftime("%Y-%m-%d-%H-%M-%S")}'
        return True

    def _value_plot(self, ax, x, y, font_size, offset):

        ax_kwgs = {
            'horizontalalignment': 'center',
            'color': self._fg,
            'fontsize': font_size
        }
        for _x, _y in zip(x, y):
            ax.text(
                _x, _y + offset, f'{int(_y)}' if self._small else f'{_y}', **ax_kwgs
            )

    def _set_spines(self, ax, label_size):
        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        ax.spines['left'].set_linewidth(2)
        ax.spines['left'].set_color(self._fg)
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['bottom'].set_color(self._fg)

        # tick setting
        ax.tick_params(direction='in', length=6, width=2, color=self._fg)
        ax.tick_params(axis='both', colors=self._fg)
        ax.tick_params(labelsize=label_size)

    def temp_plot(self, ax, offset, small=False, gray=False):
        x = self._hour
        y = self.temp

        line_width = 4 if small else 10
        marker_size = 80 if small else 400
        label_size = 14 if small else 24
        font_size = 15 if small else 32

        if gray:
            color = 'white'
        elif np.min(y) < -10:
            color = 'black'
        elif np.min(y) < 0:
            color = 'cornflowerblue'
        elif np.min(y) < 10:
            color = 'lightblue'
        elif np.min(y) < 20:
            color = 'greenyellow'
        elif np.min(y) < 30:
            color = 'pink'
        else:
            color = 'tomato'

        diff = 2
        if np.min(y) < -10:
            ymin = -15 - diff
        elif np.min(y) < -5:
            ymin = -10 - diff
        elif np.min(y) < 0:
            ymin = -5 - diff
        elif np.min(y) < 5:
            ymin = 0 - diff
        elif np.min(y) < 10:
            ymin = 5 - diff
        elif np.min(y) < 15:
            ymin = 10 - diff
        elif np.min(y) < 20:
            ymin = 15 - diff
        elif np.min(y) < 25:
            ymin = 20 - diff
        elif np.min(y) < 30:
            ymin = 25 - diff
        elif np.min(y) < 35:
            ymin = 30 - diff
        else:
            ymin = 35 - diff

        self._set_spines(ax, label_size)
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.set_ylim(ymin, ymin + 16)
        ax.plot(x, y, c=color, linewidth=line_width)
        self._value_plot(ax, x, y, font_size, offset)

        x = np.array(x)
        y = np.array(y)
        ax_kwgs = {
            'zorder': 10, 's': marker_size,
            'path_effects': [withStroke(linewidth=10, foreground='white')]
        }
        ax.scatter(
            x[y < 10], y[y < 10],
            c='white' if gray else 'mediumblue', **ax_kwgs
        )
        ax.scatter(
            x[(y >= 10) & (y < 20)], y[(y >= 10) & (y < 20)],
            c='white' if gray else 'gold',  **ax_kwgs
        )
        ax.scatter(
            x[(y >= 20) & (y < 30)], y[(y >= 20) & (y < 30)],
            c='white' if gray else 'orange', **ax_kwgs
        )
        ax.scatter(
            x[y >= 30], y[y >= 30],
            c='white' if gray else 'firebrick', **ax_kwgs
        )

    def other_plot(self, ax, y, color, ylim):
        x = self._hour
        self._set_spines(ax, 20)
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax_kwgs = {'c': color, 'linewidth': 8, }
        ax.plot(x, y, **ax_kwgs)
        ax_kwgs = {
            'zorder': 10, 'c': color, 'marker': 'o', 's': 400,
            'path_effects': [withStroke(linewidth=10, foreground='white')]
        }
        ax.scatter(x, y, **ax_kwgs)
        ax.set_xticks([])
        ax.set_ylim(ylim[0], ylim[1])
        self._value_plot(ax, x, y, 32, ylim[1] // 3)


def get_concat_h(imgs, offset):
    w, h = imgs[0].size
    dst = Image.new('RGBA', ((w + offset) * len(imgs) - offset, h + offset))
    for i, img in enumerate(imgs):
        dst.paste(img, ((w + offset) * i, offset // 2))

    return dst


def get_concat_v(img1, img2):
    dst = Image.new('RGBA', (img1.width, img1.height + img2.height))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (0, img1.height))
    return dst


def draw_img(fig, symbol, offset, img_size=160):
    fig_img = Image.fromarray(np.array(fig.canvas.renderer.buffer_rgba()))
    fw, fh = fig_img.size
    img = get_concat_h(
        [Image.open(fp).resize((img_size, img_size)) for fp in symbol],
        offset[0]
    )
    clear_img = Image.new('RGBA', (fw, fh))
    clear_img.paste(img, (offset[1], offset[2]))
    return Image.alpha_composite(fig_img, clear_img)
