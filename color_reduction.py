#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import argparse
from pathlib import Path

from PIL import Image, ImageChops


def command():
    parser = argparse.ArgumentParser(description='7色に減色する')
    parser.add_argument(
        'img', type=Path, default=None,
        help='減色する画像 [default: %(default)s]'
    )
    parser.add_argument(
        '--mode', default='rgb', metavar='RGB/HSV', choices=('rgb', 'hsv'),
        help='色判定のモードを切り替える [default:%(default)s]',
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='デバッグモード'
    )
    return parser.parse_args()


def color_from_range(i):
    return tuple([255 if j == i else 0 for j in range(3)])


def rgb_filter(r, g, b, color):
    return (
        r.point(lambda i: 1 if i > color[0] else 0, mode='1'),
        g.point(lambda i: 1 if i > color[1] else 0, mode='1'),
        b.point(lambda i: 1 if i > color[2] else 0, mode='1'),
    )


def rgb_filter_orange(r, g, b, color):
    return (
        r.point(lambda i: 1 if i > color[0] else 0, mode='1'),
        g.point(lambda i: 1 if i > color[1] else 0, mode='1'),
        b.point(lambda i: 1 if i < color[2] else 0, mode='1'),
    )


def replace_color(img, color, mask, mode='RGB'):
    img.paste(Image.new(mode, img.size, color), mask=mask)
    return img


def bit_not(img):
    return ImageChops.invert(img)


def bit_and(img1, img2):
    return ImageChops.logical_and(img1, img2)


def bit_and_and(img1, img2, img3):
    return bit_and(bit_and(img1, img2), img3)


def rgb_mode(img, debug=False):
    r, g, b = img.split()

    for i, elem in enumerate(rgb_filter(r, g, b, (120, 120, 180))):
        img = replace_color(img, color_from_range(i), elem)

    # White
    mask = bit_and_and(*rgb_filter(r, g, b, (100, 100, 100)))
    img = replace_color(img, (255, 255, 255), mask)

    if debug:
        mask.save('white_mask.png')
        img.save('white.png')

    # Orange
    mask = bit_and_and(*rgb_filter_orange(r, g, b, (180, 120, 60)))
    img = replace_color(img, (255, 128, 0), mask)

    if debug:
        mask.save('orange_mask.png')
        img.save('img.png')

    return img


def hsv_filter(h, low, upper):
    return bit_and(
        h.point(lambda i: 1 if i > low else 0, mode='1'),
        h.point(lambda i: 1 if i < upper else 0, mode='1')
    )


def hsv_mode(img, debug=False):
    img = img.convert('HSV')
    h, s, v = img.split()

    if debug:
        h.save('split_h.png')
        s.save('split_s.png')
        v.save('split_v.png')

    # Not Black
    nb = v.point(lambda i: 1 if 10 < i else 0, mode='1')
    img = nb.convert('RGB')
    if debug:
        nb.save('not_black.png')

    # White
    w = bit_and(nb, s.point(lambda i: 1 if i < 30 else 0, mode='1'))
    if debug:
        w.save('white.png')

    # Not White
    nw = bit_and(nb, bit_not(w))
    # Red
    red = bit_and(nw, bit_not(hsv_filter(h, 10, 240)))
    img = replace_color(img, (255, 0, 0), red)
    # Green
    grn = hsv_filter(h, 50, 100)
    img = replace_color(img, (0, 255, 0), grn)
    # Blue
    blu = hsv_filter(h, 150, 175)
    img = replace_color(img, (0, 0, 255), blu)
    # Orange
    org = hsv_filter(h, 10, 30)
    img = replace_color(img, (255, 128, 0), org)
    # Other(Yellow)
    buf = nw.copy()
    for i in (red, grn, blu, org):
        buf = bit_and(buf, bit_not(i))

    if debug:
        buf.save('hsv_other.png')

    img = replace_color(img, (255, 255, 0), buf)
    img = replace_color(img, (255, 255, 255), w)
    return img


def main(args):
    print(args)
    img = Image.open(args.img).convert('RGB')
    if args.mode == 'rgb':
        img = rgb_mode(img, args.debug)
    else:
        img = hsv_mode(img, args.debug)

    if args.debug:
        img.save(f'reduction_{args.mode}.png')

    return 0


if __name__ == '__main__':
    exit(main(command()))
