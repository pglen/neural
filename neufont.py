#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network load font

import sys, random, math

from PIL import Image, ImageFont, ImageDraw
#print(Image.__version__)

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut

#letters = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ " \
#            "1234567890 `~!@#$%^&*()_+{}:\"|<>?[];\'\\,./ "

space = list(" ")
#letters =  [ chr(nn) for nn in range(32) ]  + space
#letters += [ chr(nn) for nn in range(32, 64) ] + space
#letters += [ chr(nn) for nn in range(64, 96) ] + space
#letters += [ chr(nn) for nn in range(96, 128) ] + space
letters = [ chr(nn) for nn in range(128) ]
#letters = ['a', 'b', ' ']
#print(letters)

#sys.exit()
#fname = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
#fname = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
#fname = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
fname = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"

if __name__ == '__main__':

    neu =  neulut.NeuLut()

    sumx = Image.new("L", (640, 480), color=(150) )
    neu = genfonts(neu, fname, letters, sumx)
    #neu.dump()
    #print(neu)
    sumx.show()
    #sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    #sumx2.show()

# EOF
