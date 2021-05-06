#!/usr/bin/env python3
# -*-coding: utf-8 -*-
# pylint: disable=invalid-name,no-member
from PIL import Image
from pathlib import Path

USE_INKY=True
try:
    from inky.auto import auto
except ModuleNotFoundError as e:
    print(e)
    USE_INKY=False

def yellow_mask(src):#, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    mask = Image.new("1", src.size)
    w, h = src.size
    for x in range(w):
        for y in range(h):
            p = src.getpixel((x, y))
            print(p,end=', ')
            if p > 170 and p < 180:
                mask.putpixel((x, y), 255)

    return mask

def main():
    img_size = (250,122)
    if USE_INKY:
        inky_disp = auto(ask_user=True,verbose=True)
        inky_disp.set_border(inky_disp.BLACK)
        img_size = inky_disp.resolution

    print('image size:', img_size)
    for fp in Path('symbol').iterdir():
        print(fp.as_posix())
        main_img = Image.new('RGBA', img_size)
        img = Image.open(fp).resize((120,120)).convert('RGB')
        r,g,b = img.split()
        g.save(f'{fp.stem}_G.png')
        yellow_mask(g).save(f'{fp.stem}_yellow.png')
        continue
        g.save('img_G.png')
        b.save('img_B.png')
        img = Image.merge('RGB', (r,r,b)).quantize(3)
        main_img.paste(img, (100,1))
        if USE_INKY:
            inky_disp.set_image(main_img.rotate(180))
            inky_disp.show()
            break
        else:
            main_img.save(fp.name)
            break
    
    return 0


if __name__ == '__main__':
    exit(main())
