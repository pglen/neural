#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import sys, random, math

from PIL import Image, ImageFont, ImageDraw

#import trans, tenticle, neuutil

from neulib.neuutil import *
from neulib.neulut import *

verbose = 0
letters = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ " \
            "1234567890 `~!@#$%^&*()_+{}:\"|<>?[];\'\\,./ "

space = list(" ")
#letters =  [ chr(nn) for nn in range(32) ]  + space
#letters += [ chr(nn) for nn in range(32, 64) ] + space
#letters += [ chr(nn) for nn in range(64, 96) ] + space
#letters += [ chr(nn) for nn in range(96, 128) ] + space

letters = [ chr(nn) for nn in range(128) ]
#print(letters)

#sys.exit()

if __name__ == '__main__':
    print("IMG fonts")

    sumx = Image.new("L", (500,300), color=(150) )

    # use a bitmap font
    #font = ImageFont.load_default()
    #font = ImageFont.truetype(font="") # needs filename
    #font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    row = 10
    mx = 0; my = 0
    hhh = 10
    for aa in letters:
        print("letter:", aa, font.getsize(aa), end = "  ")

        fff = Image.new("L", font.getsize(aa), color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)

        sumx.paste(fff, (hhh, row,))

        hhh += font.getsize(aa)[0] + 4

        #if hhh > 450 or aa == " ":
        if hhh > 450:
            hhh = 10
            row += 20

        if mx < font.getsize(aa)[0]:
            mx = font.getsize(aa)[0]
        if my < font.getsize(aa)[1]:
            my = font.getsize(aa)[1]

        ddd = fff.getdata()

    print("\nmx", mx, "my", my)
    #sumx.show()
    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()


