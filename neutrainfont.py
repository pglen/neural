#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, random, math

from PIL import Image, ImageFont, ImageDraw

#import trans, tenticle, neuutil

from neuutil import *

import neulut
import neunp

verbose = 0
imgdir = "png"

letters = [ chr(nn) for nn in range(32, 128) ]
#print(letters)

if __name__ == '__main__':
    print("Train fonts")

    #nlut = neulut.NeuLut(200, 8)
    nlut = neunp.NeuNp(200, 8)

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new("L", (500,300), color=(150) )

    #font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    # Flatten font to linear
    row = 10; hhh = 10
    aaa = 0; bbb = 0
    #letters = "abcdefgh"
    for aa in letters:
        sss = font.getsize(aa)
        aaa += sss[0]; bbb += sss[1]
    aaa //= len(letters)
    bbb //= len(letters)

    for aa in letters:
        sss = font.getsize(aa)
        fff = Image.new("L", sss, color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)
        #scale to uniform
        #fff = fff.resize((sss[0], sss[1]))
        fff = fff.resize((aaa, bbb))

        ddd = list(fff.getdata())
        #print(aa, len(ddd), sss, ddd)
        nlut.train(ddd, aa)
        sumx.paste(fff, (hhh, row,))
        hhh += aaa + 5
        if hhh > 450:
            hhh = 10
            row += 20

    nlut.dump()

    # Recog


    sumx.paste(bw, (10, row+40,))
    sumx.paste(pp, (10, row+100,))

    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
