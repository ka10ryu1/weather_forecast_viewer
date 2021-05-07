#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import matplotlib.pyplot as plt

from util.config import command
from util.text_request import get_txt
from util.img_proc import HTML2Fig, draw_img


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
    # h2f.other_plot(
    #     fig.add_subplot(row, col, row, fc=bg),
    #     h2f.humid, 'deepskyblue', (0, 100)
    # )
    plt.tight_layout()
    fig.text(0.1, 0.91, h2f.timestamp, color=fg, fontsize=16)
    fig.canvas.draw()
    img = draw_img(fig, h2f.symbol, (15, 40, 18), 30)
    return img


def forecast_all(html_doc, symbol, dark_mode=False, row=6, col=1, tmp_row=4, font='IPAexGothic'):

    bg = 'black' if dark_mode else 'azure'
    fg = 'white' if dark_mode else 'dimgrey'

    plt.rcParams['font.family'] = font
    fig = plt.figure(figsize=(6, 6), facecolor=bg)
    plt.subplots_adjust(wspace=0.25, hspace=0.25)

    h2f = HTML2Fig(html_doc, bg, fg, base=symbol)
    h2f.temp_plot(
        fig.add_subplot(row, col, (2, tmp_row), fc=bg),
        0.5
    )
    h2f.other_plot(
        fig.add_subplot(row, col, row - 1, fc=bg),
        h2f.humid, 'deepskyblue', (0, 100)
    )
    h2f.other_plot(
        fig.add_subplot(row, col, row, fc=bg),
        h2f.wind, 'forestgreen', (0, 20)
    )
    fig.text(0.1, 0.94, h2f.timestamp, color=fg, fontsize=16)

    plt.tight_layout()
    fig.canvas.draw()
    img = draw_img(fig, h2f.symbol, (18, 55, 40))
    return img


def main(args):
    text = get_txt(args, 'forecast')
    if text is None:
        return -1

    img = forecast_all(text, args.symbol, dark_mode=args.dark)
    img.save('forecast_all.png')
    img = forecast(text, args.symbol, dark_mode=args.dark).resize((250, 122))
    img.save('forecast_small.png')
    return 0


if __name__ == '__main__':
    exit(main(command()))
