#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import sys, random, math

from PIL import Image, ImageFont, ImageDraw

#import trans, tenticle, neuutil

from neuutil import *
from neulut import *

verbose = 0
letters = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ " \
            "1234567890 `~!@#$%^&*()_+{}:\"|<>?[];\'\\,./"

if __name__ == '__main__':
    print("IMG fonts")

    sumx = Image.new("L", (500,300), color=(150) )

    # use a bitmap font
    #font = ImageFont.load_default()
    #font = ImageFont.truetype(font="Arial")
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)

    row = 10
    mx = 0; my = 0
    hhh = 10
    for aa in letters:
        print(aa, font.getsize(aa), end = "  ")

        fff = Image.new("L", font.getsize(aa), color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)

        sumx.paste(fff, (hhh, row,))

        hhh += font.getsize(aa)[0] + 4

        if hhh > 500 or aa == " ":
            hhh = 10
            row += 20

        if mx < font.getsize(aa)[0]:
            mx = font.getsize(aa)[0]
        if my < font.getsize(aa)[1]:
            my = font.getsize(aa)[1]

        ddd = fff.getdata()


    print("\nmx", mx, "my", my)
    sumx.show()
