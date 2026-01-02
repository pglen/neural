#!/usr/bin/env python

'''
     Mark boundary of letters
    Evaluate filled centers.

'''

import sys, random, math

from PIL import Image
import matplotlib.pyplot as plt

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as newlut

LOWPASS = 0

imgdir = "png"

def show(sumx, bw, pp, ppp):

    sumx.paste(bw, (10, 10))
    sumx.paste(pp, (10, bw.size[1] + 20))
    sumx.paste(ppp, (10, 2 * bw.size[1] + 30 ))
    #sumx.show()
    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

def plotvals(arrx, plotx, lab = ""):

    xx = []; yy = []
    for cnt, aa in enumerate(arrx):
        xx.append(cnt); yy.append(aa)
    plotx.plot(xx, yy, label=lab)

def plotflags(fallx, arrx, plotx, nulval = 0, lab = ""):

    xxx = []; yyy = []
    for ccc in range(len(arrx)):
        if fallx[ccc]:
            flag = arrx[ccc]
            xxx.append(ccc); yyy.append(flag)
    plotx.scatter(xxx, yyy, label=lab)

if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    ppp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new(bw.mode, (300, 200), color=240)

    arr = list(bw.getdata())

    # Verify
    #for cnt in range(len(arr)):
    #    aa, bb = cnt % bw.size[0], cnt // bw.size[0]
    #    pp.putpixel((aa, bb), arr[cnt])
    #show(sumx, bw, pp, ppp)
    #sys.exit(0)

    # Plot
    #plotvals(arr, plt, "Org")
    #plotvals(lll, plt, "LowPass")
    #plotflags(hraised, arr, plt, -100, 'Rise')
    #plotflags(falls, arr, plt, -200, 'Fall')
    #plt.xlabel("X Values"); plt.ylabel("Y Sums")
    #plt.legend()
    #plt.show()
    #sys.exit(0)

    hfalls = falledges(arr, bw.size)
    for cnt, cc in enumerate(hfalls):
        if cc:
            pp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)
            ppp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    hraised = raisededges(arr, bw.size)
    for cnt, cc in enumerate(hraised):
        if cc:
            pp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 180)
            ppp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 180)

    vraised = vraisededges(arr, bw.size)
    for cnt, cc in enumerate(vraised):
        if cc:
            ppp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    vfall = vfalledges(arr, bw.size)
    for cnt, cc in enumerate(vfall):
        if cc:
            ppp.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 180)

    # Output it
    #for cnt, cc in enumerate(crosses):
    #    pp.putpixel(cc, 100)
    #

    show(sumx, bw, pp, ppp)

# EOF
