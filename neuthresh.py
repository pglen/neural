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
from pgdict import *
import neulut

LOWPASS = 0
imgdir = "png"

cntx = 0
basex = []
letter = []

def scale(lettx, newx, newy, ppp = None):

    rows = [] ; cols = []

    #print(lettx)

    for nx, ny, val in lettx:
        if nx not in cols:
            cols.append(nx)
        if ny not in rows:
            rows.append(ny)
    aspx =  newx /len(cols)   ; aspy =   newy / len(rows)
    #print("aspx %.3f" % aspx, "aspy %.3f" % aspy, "new:",
    #                newx, "old", len(cols), newy, len(rows))
    ret = []
    for aa in range(newx):
        offs = len(rows) * aa
        for bb in range(newy):
            try:
                bbb = bb / aspx
                aaa = aa / aspy
                #print("%.3f " % aaa, "%.3f " %bbb, int(aaa), int(bbb))
                val = lettx[int(bbb + offs)] [2]
            except IndexError:
                #print(bbb, aaa, sys.exc_info())
                pass
            except:
                print(sys.exc_info())
            ret.append((aa, bb, val))
    if ppp:
        for aa, bb, val in ret:
            ppp.putpixel((aa, bb), val)
            pass
    #print(len(ret))
    return ret

def callme(keys, val):
    global cntx, basex, cols, rows
    if keys[0] == 0 and keys[1] == 0:
        if cntx == 0:
            basex = keys[2], keys[3]

        nx = keys[2]-basex[0];  ny = keys[3]-basex[1]
        dd.putpixel((nx, ny), val)
        letter.append((nx, ny, val))

        print("%s %3d" % (keys, val),  end = "  ")
        if cntx % 3 == 2:
            print()
        cntx += 1

if __name__ == '__main__':

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    pp = Image.new(bw.mode, bw.size, color=255)
    dd = Image.new(bw.mode, bw.size, color=255)
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
    ''' plotvals(arr, plt, "Org")
    plotvals(lll, plt, "LowPass")
    plotflags(thh, thh, plt, -100, '1')
    plt.xlabel("X Step"); plt.ylabel("Y Sums")
    plt.legend()
    plt.show()
    sys.exit(0)
    '''

    # Output it
    ret = sections(thh, thh2, bw) #, pp)
    ret.recurse(callb = callme)
    print()
    # normalize
    scale(letter, 10, 17, pp)

    sumx.paste(bw)
    sumx.paste(pp, (0, (bw.size[1] + 5) * 1))
    #sumx.paste(pp, ((bw.size[0] + 5), (bw.size[1] + 5) * 1))
    sumx.paste(dd, (0, (bw.size[1] + 5) * 2))
    #sumx.paste(dd, ((bw.size[0] + 5), (bw.size[1] + 5) * 2))

    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
