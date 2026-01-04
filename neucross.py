#!/usr/bin/env python

'''
    Mark boundary of letters
    Evaluate centers.
'''

import sys, random, math

from PIL import Image
import matplotlib.pyplot as plt

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut

LOWPASS = 0

imgdir = "png"

bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))

pp0 = Image.new(bw.mode, bw.size, color=255)
pp1 = Image.new(bw.mode, bw.size, color=255)
pp2 = Image.new(bw.mode, bw.size, color=255)
pp3 = Image.new(bw.mode, bw.size, color=255)
pp4 = Image.new(bw.mode, bw.size, color=255)

def show(sumx, bw):

    sumx.paste(bw, (10, 10))
    sumx.paste(pp0, (120, 10))

    sumx.paste(pp1, (10, bw.size[1] + 20))
    sumx.paste(pp2, (10, 2 * bw.size[1] + 30 ))

    sumx.paste(pp3, (120, bw.size[1] + 20 ))
    sumx.paste(pp4, (120, 2 * bw.size[1] + 30 ))

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

    sumx = Image.new(bw.mode, (300, 200), color=240)
    arr = list(bw.getdata())

    fname = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
    neu =  neulut.NeuLut()
    letters = [ chr(nn) for nn in range(ord('a'), ord('z')+1) ]
    neu = genfonts(neu, fname, letters) #, sumx)

    # Verify
    #for cnt in range(len(arr)):
    #    aa, bb = cnt % bw.size[0], cnt // bw.size[0]
    #    pp.putpixel((aa, bb), arr[cnt])
    #show(sumx, bw)
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

    hraised = raisededges(arr, bw.size)
    for cnt, cc in enumerate(hraised):
        if cc:
            pp1.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 128)
            pp2.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    hfall = falledges(arr, bw.size)
    for cnt, cc in enumerate(hfall):
        if cc:
            pp1.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)
            pp2.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    vraised = vraisededges(arr, bw.size)
    for cnt, cc in enumerate(vraised):
        if cc:
            pp2.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)
            pp3.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    vfall = vfalledges(arr, bw.size)
    for cnt, cc in enumerate(vfall):
        if cc:
            pp3.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 128)
            pp2.putpixel((cnt % bw.size[0], cnt // bw.size[0]), 0)

    #ccc3  = load_font_img("png/letter_a.png")
    #ccc2 = load_font_img("png/letter_b.png")
    #ccc = load_font_img("png/letter_c.png")
    #fl = len(list(ccc.getdata()))

    #sumx.paste(ccc3, (10, 10))
    #sumx.paste(ccc2, (10, 30))
    #sumx.paste(ccc,  (10, 50))
    #sumx.show()
    #sys.exit(0)

    #nn = neulut.NeuLut()
    #
    ## All white and all black
    #nn.memorize([ 0 for nn in range(fl) ],  (" ",))
    ##nn.memorize([ 255 for nn in range(fl) ],  ("-",))
    #
    #nn.memorize(list(ccc.getdata()),  ("c",))
    #nn.memorize(list(ccc2.getdata()), ("b",))
    #nn.memorize(list(ccc3.getdata()), ("a",))

    # Cross product of the edges
    #crosses = crossfunc(hfall, vfall)
    crosses = crossfunc(hraised, vraised)
    for cnt, cc in enumerate(crosses):
        if cc:
            xx, yy = (cnt % bw.size[0], cnt // bw.size[0])
            pp4.putpixel((xx, yy), 0)
            arr2 = arr[cnt:]:
            yyy = 0 ; xxx = 0

            for aa in range(100):
                arr[cnt:]:
                pp4.putpixel((xxx, yyy), 0)
                xxx += 1
                if xxx > yyy


            fff = neu.recall(arr[cnt:], bw.size[0])
            print(fff, xx, yy)

    show(sumx, bw)

# EOF
