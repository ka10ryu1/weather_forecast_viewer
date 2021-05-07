#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path

USE_INKY = True
try:
    from inky.auto import auto
except ModuleNotFoundError as e:
    print(e)
    USE_INKY = False


# , mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
def yellow_mask(src):
    _y = Image.new('1', src.size)
    _w = Image.new('1', src.size)

    w, h = src.size
    colors = []
    for x in range(w):
        for y in range(h):
            p = src.getpixel((x, y))
            colors.append(p)
            if p < 60:
                _y.putpixel((x, y), 255)
            elif 100 < p:
                _w.putpixel((x, y), 255)

    print(sorted(list(set(colors))))
    return _y, _w


def convert_img(white, yellow, img_size):
    img = Image.new('P', img_size)
    w, h = img.size
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            val_w = white.getpixel(pos)
            val_y = yellow.getpixel(pos)
            if val_w > 100:
                img.putpixel(pos, 0)
            elif val_y > 100:
                img.putpixel(pos, 2)
            else:
                img.putpixel(pos, 1)

    return img


def main():
    img_size = (250, 122)
    if USE_INKY:
        inky_disp = auto(ask_user=True, verbose=True)
        inky_disp.set_border(inky_disp.BLACK)
        img_size = inky_disp.resolution

    out = Path('out')
    out.mkdir(parents=True, exist_ok=True)
    print('image size:', img_size)

    for fp in Path('symbol').iterdir():
        print(fp.as_posix())
        img = Image.open(fp).resize((120, 120)).convert('RGB')
        r, g, b = img.split()
        y, w = yellow_mask(b)

        if USE_INKY:
            img = convert_img(w, y, img_size)
            inky_disp.set_image(img.rotate(180))
            inky_disp.show()
            break
        else:
            y.save(out / f'{fp.stem}_yellow.png')
            w.save(out / f'{fp.stem}_white.png')

    return 0


if __name__ == '__main__':
    exit(main())
