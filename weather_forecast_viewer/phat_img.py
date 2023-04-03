#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import time
import argparse
from PIL import Image
from pathlib import Path

USE_INKY = True
try:
    from inky.auto import auto
except ModuleNotFoundError as e:
    print(e)
    USE_INKY = False


def command():
    parser = argparse.ArgumentParser(description='天気表示')
    parser.add_argument(
        '-i', '--img', type=Path,
        help='input image [default: %(default)s]'
    )
    args = parser.parse_args()
    return args


def yellow_mask(img, max_val=255):
    _, _, src = img.split()
    _y = Image.new('1', src.size)
    _w = Image.new('1', src.size)

    w, h = src.size
    colors = []
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            p = src.getpixel(pos)
            colors.append(p)
            if 40 < p and p < 70:
                if y < 14 or 34 < y:
                    continue

                _y.putpixel(pos, max_val)
            elif 100 < p:
                _w.putpixel(pos, max_val)

    print('yellow mask:', sorted(list(set(colors))))
    return _y, _w, src


def convert_img(white, yellow, img_size):
    img = Image.new('P', img_size)
    w, h = white.size
    cnt = [0, 0]
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            val_w = white.getpixel(pos)
            val_y = yellow.getpixel(pos)
            # print(white.size, yellow.size, img.size, pos, val_w, val_y)
            if val_w > 100:
                cnt[0] += 1
                img.putpixel(pos, 0)
            elif val_y > 100:
                cnt[1] += 1
                img.putpixel(pos, 2)
            else:
                img.putpixel(pos, 1)

    print('convert img:', cnt)
    return img


def test():
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
        img = Image.open(fp).resize((100, 100)).convert('RGB')
        y, w = yellow_mask(img)

        if USE_INKY:
            img = convert_img(w, y, img_size)
            inky_disp.set_image(img.rotate(180))
            inky_disp.show()
            time.sleep(30)
        else:
            y.save(out / f'{fp.stem}_yellow.png')
            w.save(out / f'{fp.stem}_white.png')

    return 0


def main(args):
    if args.img is None:
        return test()

    img_size = (250, 122)
    if USE_INKY:
        inky_disp = auto(ask_user=True, verbose=True)
        inky_disp.set_border(inky_disp.BLACK)
        img_size = inky_disp.resolution

    out = Path('out')
    out.mkdir(parents=True, exist_ok=True)
    print('image size:', img_size)
    print(args.img.as_posix())
    img = Image.open(args.img).convert('RGB')
    y, w, b = yellow_mask(img)

    if USE_INKY:
        img = convert_img(w, y, img_size)
        inky_disp.set_image(img.rotate(180))
        inky_disp.show()
        time.sleep(30)
    else:
        img.save(out / f'{args.img.stem}_org.png')
        b.save(out / f'{args.img.stem}_b.png')
        y.save(out / f'{args.img.stem}_yellow.png')
        w.save(out / f'{args.img.stem}_white.png')

    return 0


if __name__ == '__main__':
    exit(main(command()))
