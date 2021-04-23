#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import matplotlib.pyplot as plt

from util import command
from text_request import get_txt
from img_proc import HTML2Fig, draw_img


def forecast(html_doc, dark_mode=False, row=4, col=1, tmp_row=3, font='Meiryo'):

    bg = 'black' if dark_mode else 'azure'
    fg = 'white' if dark_mode else 'dimgrey'

    plt.rcParams['font.family'] = font
    fig = plt.figure(figsize=(7, 3), facecolor=bg)
    plt.subplots_adjust(wspace=0.25, hspace=0.25)

    h2f = HTML2Fig(html_doc, bg, fg)
    h2f.temp_plot(
        fig.add_subplot(row, col, (2, tmp_row), fc=bg),
        2
    )
    h2f.other_plot(
        fig.add_subplot(row, col, row, fc=bg),
        h2f.humid, 'deepskyblue', (0, 100)
    )
    plt.tight_layout()
    fig.text(0.1, 0.91, h2f.timestamp, color=fg)
    fig.canvas.draw()
    draw_img(fig, h2f.symbol, (22, 48, 24), 60)
    return 0


def forecast_all(html_doc, dark_mode=False, row=6, col=1, tmp_row=4, font='Meiryo'):

    bg = 'black' if dark_mode else 'azure'
    fg = 'white' if dark_mode else 'dimgrey'

    plt.rcParams['font.family'] = font
    fig = plt.figure(figsize=(6, 6), facecolor=bg)
    plt.subplots_adjust(wspace=0.25, hspace=0.25)

    h2f = HTML2Fig(html_doc, bg, fg)
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
    fig.text(0.1, 0.94, h2f.timestamp, color=fg)

    plt.tight_layout()
    fig.canvas.draw()
    draw_img(fig, h2f.symbol, (18, 55, 40))
    return 0


def main(args):
    if (text := get_txt(args, 'forecast')) is None:
        return -1

    forecast_all(text, dark_mode=args.dark)
    forecast(text, dark_mode=args.dark)
    return 0


if __name__ == '__main__':
    exit(main(command()))
