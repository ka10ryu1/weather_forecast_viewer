#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path

from inky.auto import auto

def main():
    inky_disp = auto(ask_user=True,verbose=True)
    inky_disp.set_border(inky_disp.BLACK)
    for fp in Path('symbol').iterdir():
        main_img = Image.new('RGBA',inky_disp.resolution)
        print('RGBA',inky_disp.resolution,main_img.size)

        print(fp.as_posix())
        img = Image.open(fp).resize((120,120))
        main_img.paste(img, (100,1))
        inky_disp.set_image(main_img)
        inky_disp.show()
        break

    return 0


if __name__ == '__main__':
    exit(main())
