#!/usr/bin/env python

# ------------------------------------------------------------------------
# Mark boundary of letters

'''
    Evaluate letter centers.

'''

import sys, random, math

from PIL import Image
import matplotlib.pyplot as plt

from neuutil import *
from pgutil import *
import neulut

LOWPASS = 2


def plotvals(arrx, plotx, lab = ""):
    xx = []; yy = []
    for cnt, aa in enumerate(arrx):
        xx.append(cnt); yy.append(aa)
    plotx.plot(xx, yy, label=lab)

def plotflags(fallx, arrx, nulval):

    xxx = []; yyy = []
    for ccc in range(len(arrx)):
        if fallx[ccc]:
            flag = arrx[ccc]
            xxx.append(ccc); yyy.append(flag)
    return xxx, yyy

imgdir = "png"

if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))

    arr = []
    for aa in range(0, bw.size[1], 1):
        sss = 0
        for bb in range(0, bw.size[0], 1):
            pxx = 255 - bw.getpixel((bb, aa))  # white is zero
            sss += pxx
        arr.append(sss)
    lll = lowpass(arr, LOWPASS)
    falls = falledges(lll)
    raised = raisededges(lll)

    arr2 = []
    for xx in range(0, bw.size[0], 1):
        ssss = 0
        for yy in range(0, bw.size[1], 1):
            pxx2 = 255 - bw.getpixel((xx, yy))  # white is zero
            ssss += pxx2
        arr2.append(ssss)
    lll2 = lowpass(arr2, LOWPASS)
    falls2 = falledges(lll2)
    raised2 = raisededges(lll2)

    # Plot
    plotvals(arr, plt, "Org")
    plotvals(lll, plt, "LowPass")

    plt.scatter(*plotflags(raised, lll, -400), label='Rise')
    plt.scatter(*plotflags(falls, lll, -200), label='Fall')
    plt.xlabel("X Values"); plt.ylabel("Y Sums")
    plt.legend()

    plt.show()
    sys.exit(0)

    for cnt, cc in enumerate(raised):
        if cc:
            for bbb in range(0, bw.size[0], 1):
                #print(pxx, end = " ")
                bw.putpixel((bbb, cnt), 100)

    for cnt, cc in enumerate(raised2):
        if cc:
            for bbb in range(0, bw.size[1], 1):
                #print(pxx, end = " ")
                bw.putpixel((cnt, bbb), 100)

    bw.show()

# EOF
