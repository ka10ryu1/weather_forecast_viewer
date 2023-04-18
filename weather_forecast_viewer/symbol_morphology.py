#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
import argparse
from pathlib import Path

import cv2
import numpy as np


def command():
    parser = argparse.ArgumentParser(description='アイコンに白い縁取りを実施する')
    parser.add_argument(
        'imgs', type=Path, nargs='+',
        help='縁取りする画像'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='デバッグモード'
    )
    return parser.parse_args()


def imshow(name, img):
    img = cv2.resize(img, (256, 256))
    cv2.imshow(name, img)


def add_contours(img, alpha1, alpha2):
    alpha = cv2.absdiff(alpha2, alpha1)
    alpha = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)[1]
    return cv2.add(img, alpha)


def main(args):
    print(args)
    for path in args.imgs:
        img = cv2.imread(path.as_posix(), cv2.IMREAD_UNCHANGED)
        print(path.as_posix(), img.shape)
        if img.shape[-1] != 4:
            print('Alpha color not found')
            continue

        b, g, r, a1 = cv2.split(img)
        a2 = cv2.dilate(a1, np.ones((3, 3), np.uint8), iterations=1)
        a2 = cv2.threshold(a2, 180, 255, cv2.THRESH_BINARY)[1]
        b = add_contours(b, a1, a2)
        g = add_contours(g, a1, a2)
        r = add_contours(r, a1, a2)
        dst_img = cv2.merge((b, g, r, a2))
        if args.debug:
            imshow('test b', b)
            imshow('test g', g)
            imshow('test r', r)
            imshow(dst_img)
            cv2.waitKey(5000)

        cv2.imwrite(path.name, dst_img)

    return 0


if __name__ == '__main__':
    exit(main(command()))
