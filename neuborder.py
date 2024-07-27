#!/usr/bin/env python

# ------------------------------------------------------------------------
# Mark boundary of letters

'''
    Evaluate letter boundaries. Grid method.

'''

import sys, random, math

from PIL import Image

#import trans, tenticle, neuutil

from neuutil import *
from pgutil import *
import neulut

imgdir = "png"

if __name__ == '__main__':

    #sumx = Image.new("L", (800,600), color=(100) )

    bw = load_bw_image(os.path.join(imgdir,"srect_white_abc.png"))

    #for aa in range(0, bw.size[1], 1):
    #    for bb in range(0, bw.size[0], 1):
    #        pxx = bw.getpixel((bb, aa),)
    #        bw.putpixel((bb, aa,), pxx+200)

    # Histogram
    freq = [0 for _ in range(256) ]
    for aa in range(0, bw.size[1], 1):
        for bb in range(0, bw.size[0], 1):
            pxx = 255 - bw.getpixel((bb, aa),)  # white is zero
            freq[pxx] += 1
    old = 0; ocnt = 0
    for cnt, aa in enumerate(freq):
        #if aa > 0:
        #    print(cnt, "\t", aa)
        if old < aa:
            old = aa; ocnt = cnt

    print("background color:", ocnt)
    #print(freq); ocnt = 0
    #sys.exit(0)

    arr = []
    for aa in range(0, bw.size[1], 1):
        sss = 0
        for bb in range(0, bw.size[0], 1):
            pxx = 255 - bw.getpixel((bb, aa))  # white is zero
            #print(pxx, end = " ")
            #bw.putpixel((bb, aa,), 10)
            sss += pxx
            #if aa > 20:
            #    break
        #print(aa, sss, end = " " )
        arr.append(sss)

    arr2 = []
    for xx in range(0, bw.size[0], 1):
        ssss = 0
        for yy in range(0, bw.size[1], 1):
            pxx2 = 255 - bw.getpixel((xx, yy))  # white is zero
            #bw.putpixel((xx, yy,), 10)
            ssss += pxx2
        #print(xx, ssss, end = " - " )
        arr2.append(ssss)

    #print(arr)
    #print(arr2)

    for cnt, cc in enumerate(arr):
        if cc < 100:
            for bbb in range(0, bw.size[0], 1):
                #print(pxx, end = " ")
                bw.putpixel((bbb, cnt), 100)

    for cnt, dd in enumerate(arr2):
        if dd < 100:
            for bbb in range(0, bw.size[1], 1):
                #print(pxx, end = " ")
                bw.putpixel((cnt, bbb), 100)

    bw.show()

# EOF
