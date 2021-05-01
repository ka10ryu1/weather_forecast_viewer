#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path

from inky.auto import auto

from util.config import command
from util.text_request import get_txt
from util.main_img import forecast

def main(args):
    print('Get weather forecast data...')
    text = get_txt(args, 'forecast')
    if text is None:
        return -1

    print('Detect inky module...')
    inky_disp = auto(ask_user=True,verbose=True)
    inky_disp.set_border(inky_disp.WHITE)
    print('pHat Display Size:',inky_disp.resolution)

    img = forecast(text,dark_mode=True,font='IPAexGothic').resize(inky_disp.resolution).convert('L')
    inky_disp.set_image(img)
    inky_disp.show()

    return 0


if __name__ == '__main__':
    exit(main(command()))
