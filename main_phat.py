#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path

from inky.auto import auto

from util.config import command
from util.text_request import get_txt
from main_img import forecast
from phat_img import yellow_mask, convert_img

def main(args):
    print('Get weather forecast data...')
    text = get_txt(args, 'forecast')
    if text is None:
        return -1

    print('Detect inky module...')
    inky_disp = auto(ask_user=True, verbose=True)
    inky_disp.set_border(inky_disp.WHITE)
    inky_size = inky_disp.resolution
    print('pHat Display Size:', inky_size)

    img = forecast(text, args.symbol, dark_mode=True, font='IPAexGothic').resize(inky_size).convert('RGB')
    print(img.size)
    y, w, _ = yellow_mask(img)
    img = convert_img(w, y, inky_size)
    inky_disp.set_image(img.rotate(180))
    inky_disp.show()

    return 0


if __name__ == '__main__':
    exit(main(command()))
