#!/usr/bin/env python

# ------------------------------------------------------------------------
# Mark boundary of letters

'''
    Evaluate filled centers.

'''

import sys, random, math

from PIL import Image
import matplotlib.pyplot as plt

from neuutil import *
from pgutil import *
import neulut

LOWPASS = 0
imgdir = "png"


if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new(bw.mode, (300, 200), color=240)

    arr = []
    for aa in range(0, bw.size[1], 1):
        sss = 0
        for bb in range(0, bw.size[0], 1):
            pxx = 255 - bw.getpixel((bb, aa))  # white is zero
            sss += pxx
        arr.append(sss)
    lll = lowpass(arr, LOWPASS)

    thh = []
    for cnt, aa in enumerate(lll):
        thh.append(aa > 10)
    #print(thh)

    arr2 = []
    for xx in range(0, bw.size[0], 1):
        ssss = 0
        for yy in range(0, bw.size[1], 1):
            pxx2 = 255 - bw.getpixel((xx, yy))  # white is zero
            ssss += pxx2
        arr2.append(ssss)
    lll2 = lowpass(arr2, LOWPASS)

    thh2 = []
    for cnt, aa in enumerate(lll2):
        thh2.append(aa > 10)
    #print(thh2)

    # Plot
    plotvals(arr, plt, "Org")
    plotvals(lll, plt, "LowPass")
    plotflags(thh, thh, plt, -100, '1')
    plt.xlabel("X Step"); plt.ylabel("Y Sums")
    plt.legend()
    #plt.show()
    #sys.exit(0)

    # Output it
    sections(thh, thh2, bw, pp)

    sumx.paste(bw)
    sumx.paste(pp, (0, bw.size[1] + 5))
    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
