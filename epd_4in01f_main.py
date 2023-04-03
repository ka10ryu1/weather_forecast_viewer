#!/usr/bin/python3
# -*- coding:utf-8 -*-
import socket
from PIL import Image, ImageDraw, ImageFont

from util.config import command
from util.epd4in01f import EPD
from util.text_request import get_some_txt
from color_reduction import hsv_mode
from main_img import forecast_all, draw_footer


def get_host_name():
    return socket.gethostname()


def get_ip_address():
    connect_interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connect_interface.connect(('8.8.8.8', 80))
    ip_address = connect_interface.getsockname()[0]
    connect_interface.close()
    return ip_address


def main(args):

    epd = EPD()
    epd.init()
    epd.Clear()

    if args.debug:
        path = args.symbol / '4in01-1.bmp'
        if not path.exists():
            print(f'path not found: {path.as_posix():}')
            return -1

        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        draw_kwgs = {
            'font': ImageFont.truetype('NotoSansMono-Regular.ttf', 28),
            'fill': epd.GREEN,
        }
        draw.text(
            (250, 270), f'{get_host_name()}:{get_ip_address()}', **draw_kwgs)

    else:
        text = get_some_txt(args, ['forecast', 'weather'])
        if text is None:
            return -1

        img = forecast_all(
            text['forecast'], args.symbol, dark_mode=args.dark
        ).resize((640, 360))
        img = draw_footer(img, args.symbol, text['weather'])
        img = hsv_mode(img)

    epd.display(epd.getbuffer(img.rotate(180)))
    return 0


if __name__ == '__main__':
    exit(main(command()))
