#!/usr/bin/env python

'''
    test lowpass filter
'''

import os, sys, random, math

from PIL import Image
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
#print(sys.path)

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as newlut

LOWPASS = 0

imgdir = "png"

def show(sumx, bw, pp):

    sumx.paste(bw, (10, 10))
    sumx.paste(pp, (10, bw.size[1] + 20))
    #sumx.show()
    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new(bw.mode, (300, 200), color=240)

    arr = list(bw.getdata())
    lll = lowpass(arr)

    # Verify
    for cnt in range(len(lll)):
        aa, bb = cnt % bw.size[0], cnt // bw.size[0]
        #print("cnt", aa, bb)
        pp.putpixel((aa, bb), lll[cnt])
    show(sumx, bw, pp)
    sys.exit(0)

# EOF
