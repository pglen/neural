#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import sys, random, math

from PIL import Image, ImageFont, ImageDraw

#import trans, tenticle, neuutil

from neuutil import *
from neulut import *

verbose = 0
letters = [ chr(nn) for nn in range(128) ]
#print(letters)

if __name__ == '__main__':
    print("Train fonts")

    nlut = NeuLut(200, 8)

    sumx = Image.new("L", (500,300), color=(150) )

    #font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    # Flatten font to linear
    letters = "abcdefgh"
    for aa in letters:
        sss = font.getsize(aa)
        fff = Image.new("L", sss, color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)
        ddd = list(fff.getdata())
        #print(aa, len(ddd), sss, ddd)
        nlut.train(ddd, aa)

    nlut.dump()
    sys.exit()

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

        if hhh > 450 or aa == " ":
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


# EOF
