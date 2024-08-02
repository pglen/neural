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
    falls = falledges(lll)
    hraised = raisededges(lll)

    # Plot
    plotvals(arr, plt, "Org")
    plotvals(lll, plt, "LowPass")
    plotflags(hraised, lll, plt, -100, 'Rise')
    plotflags(falls, lll, plt, -200, 'Fall')
    plt.xlabel("X Values"); plt.ylabel("Y Sums")
    plt.legend()
    #plt.show()
    #sys.exit(0)

    arr2 = []
    for xx in range(0, bw.size[0], 1):
        ssss = 0
        for yy in range(0, bw.size[1], 1):
            pxx2 = 255 - bw.getpixel((xx, yy))  # white is zero
            ssss += pxx2
        arr2.append(ssss)
    lll2 = lowpass(arr2, LOWPASS)
    falls2 = falledges(lll2)
    vraised = raisededges(lll2)

    crosses = []
    for cnt, cc in enumerate(hraised):
        if cc:
            for bbb in range(0, bw.size[0], 1):
                # if vertical contains this point, it is a crossing
                if vraised[bbb]:
                    crosses.append((bbb, cnt))

    #for cnt, cc in enumerate(falls):
    #    if cc:
    #        for bbb in range(0, bw.size[0], 1):
    #            #print(pxx, end = " ")
    #            bw.putpixel((bbb, cnt), 200)

    #for cnt, cc in enumerate(vraised):
    #    if cc:
    #        for bbb in range(0, bw.size[1], 1):
    #            #print(pxx, end = " ")
    #            bw.putpixel((cnt, bbb), 100)

    # Output it
    for cnt, cc in enumerate(crosses):
        pp.putpixel(cc, 100)

    for cnt, cc in enumerate(crosses):
        bw.putpixel(cc, 100)
        #bw.putpixel((cc[0], cc[1] + 1), 100)
        #bw.putpixel((cc[0], cc[1] - 1), 0)

    sumx.paste(bw)
    sumx.paste(pp, (0, bw.size[1] + 5))
    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
