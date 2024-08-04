#!/usr/bin/env python

import sys, random, time

from PIL import Image

from collections import defaultdict
recursivedict = lambda: defaultdict(recursivedict)

def pn(num):
    return "% -7.3f" % num

# ------------------------------------------------------------------------

# Deliver a random member of an array

def randmemb(var):
    if type(var) != type( () ) and type(var) != type([]) :
        raise ValueError("Must be a list / array")
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

# ------------------------------------------------------------------------
# Deliver a random number in range of 0 to +1

def neurand():
    ret = random.random();
    #print "%+0.3f " % ret,
    return ret

def neurand2():
    ret = random.random() * 2 - 1;
    #print("neurand %+0.3f " % ret)
    return ret

def sqr(vvv):
    return vvv * vvv

def parr(arr):
    for aa in arr:
        print(pn(aa), end = " ")

    print()

def is_ok(val, ref):
    if val == ref:
        ret = "\033[32;1mOK\033[0m"
    else:
        ret = "\033[31;1mERR\033[0m"
    return ret

def newarr(size, fill):
    arrx = []
    for ee in range(size):
        arrx.append(fill)
    return arrx

def load_font_img(fname):

    arr = []; arr2 = []
    aaa = Image.open(fname)
    #print(aaa.format, aaa.size, aaa.mode, aaa.getbands())
    mmm = aaa.size[0]; eee = 0
    for aa in range(aaa.size[1]):
        mark = 0
        for bb in range(aaa.size[0]):
            xxx = aaa.getpixel((bb, aa,))
            #print (xxx, end=" ")

            if xxx != (255, 255, 255, 255):
                mark = 1
        if not mark:
            for bb in range(aaa.size[0]):
                #aaa.putpixel((bb, aa,), ( 255, 0, 255))
                pass
        else:
            begx = 0; endx = 0
            for bb in range(aaa.size[0]):
                xxx = aaa.getpixel((bb, aa,))
                if xxx != (255, 255, 255, 255):
                    begx = bb
                    break

            for bb in range(aaa.size[0]-1, -1, -1):
                xxx = aaa.getpixel((bb, aa,))
                if xxx != (255, 255, 255, 255):
                    endx = bb
                    break
                #aaa.putpixel((bb, aa,), ( 255, 255, 122))

            mmm = min(mmm, begx)
            eee = max(eee, endx)
            arr2. append(aa)
            #print(bb, begx, endx)

    for aa in arr2:
        for zz in range(mmm, eee):
            pix = aaa.getpixel((zz, aa,))
            if pix ==  (255, 255, 255, 255):
                pix = 255
            else:
                pix = 0
            arr.append(pix)

    #print(arr)
    #print(fname, eee-mmm, "x", len(arr2))
    #print("new", "L", eee-mmm, len(arr2), "data len", len(arr))

    ccc = Image.new("L", (eee-mmm, len(arr2)))
    ccc.putdata(arr)
    #ccc.show()

    #nsize = (eee-mmm) * len(arr2)

    return ccc


def load_bw_image(fname):

    im = Image.open(fname)
    #print(im.format, im.size, im.mode, im.getbands())

    arr3 = []
    for aa in range(im.size[1]):
        for bb in range(im.size[0]):
            pix = im.getpixel((bb, aa,))
            #print(pix)
            if pix ==  (255, 255, 255, 255):
                pix = 255
            else:
                pix = 0

            arr3.append(pix)

    bw = Image.new("L", im.size, color=(255) )
    bw.putdata(arr3)

    return bw

def lowpass(arrx, factorx = 1):

    ''' low pass filter '''

    lll = arrx[:]
    lenx = len(lll)
    for _ in range(factorx):
        # first and last unchanged
        for ddd in range(1, lenx-2):
            avg = lll[ddd-1] + lll[ddd] + lll[ddd+1]
            lll[ddd] = avg // 3
    return lll

def falledges(arrx):

    ''' detect falling edges '''

    lenx = len(arrx)
    prev = 0; fall = 0
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if arrx[ddd] < prev:
            if not fall:
                fall = True
                eee[max(0, ddd-1)] = True
        else:
            fall = False
        prev = arrx[ddd]
    return eee

def raisededges(arrx):

    ''' detect falling edges '''

    lenx = len(arrx)
    prev = 0; fall = 0
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if arrx[ddd] > prev:
            if not fall:
                fall = True
                eee[max(0, ddd-1)] = True
        else:
            fall = False
        prev = arrx[ddd]
    return eee

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

from pgdict import *

def sections(thh1x, thh2x, bww, ppp):

    ''' Boundary by non zero sectons '''

    ret = DeepDict()

    prog = 0; xlen = len(thh2x); curr = 0
    while True:
        if prog >=  xlen:
            break
        if thh2x[prog]:
            while True:
                if prog >=  xlen:
                    break
                if  not thh2x[prog]:
                    #print()
                    break
                # one X section
                bww.putpixel((prog, 0), 200)
                #print(prog, end = " ")
                _sectiony(thh1x, prog, curr, ret, bww, ppp)
                prog += 1
            curr += 1
            #break
        prog += 1
    #for aa in ret:
    #    for bb in ret[aa]:
    #        #print(aa, bb)
    #        for cc in ret[aa][bb]:
    #            #print(aa, bb, cc) #ret[aa][bb][cc])
    #            for dd in ret[aa][bb][cc]:
    #                print("[%d, %d, %d, %d] %d" % (aa,bb,cc,dd, ret[aa][bb][cc][dd]) )
    #def callme(keys, val):
    #    print(keys, val)
    #ret.recurse(callb = callme)
    #print(ret)
    return ret

def _sectiony(arry, xx, currx, ret, bww, ppp):
    progy = 0; leny = len(arry);  curry = 0;
    while True:
        if progy >= leny:
            break
        if arry[progy]:
            while(True):
                if not arry[progy]:
                    break
                #bww.putpixel((0, progy),  200)
                col = bww.getpixel((xx, progy))
                ppp.putpixel((xx, progy), 200 - col)
                ret.setdeep((currx,curry,xx,progy), col)
                #ret[currx,curry,xx,progy] = col
                #print(currx,curry,xx,progy, col)
                progy += 1
            #print("[", xx, prog, end = " ] " )
            curry += 1
            #break
        progy += 1

# Decorator for speed measure
def measure(func):
    def run(*args, **kwargs):
        ttt = time.time()
        ret = func(*args, **kwargs)
        print("Exe: %.3f us" % ((time.time() - ttt) * 1000000))
        return ret
    return run

def rle(arr):

    ''' run length encoding '''

    arr2 = []; cntx = 1
    if not len(arr):
        return arr2

    prev = arr[0];
    for bb in arr:
        if prev != bb:
            if cntx == 1:
                arr2.append(prev)
            else:
                arr2.append((cntx, prev))
            prev = bb
            cntx = 1
        else:
            cntx += 1
    return arr2

            # EOF

