#!/usr/bin/env python

import random
from PIL import Image

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

    lenx = len(arrx)
    lll = [0 for _ in range(lenx) ]
    # first and last unchanged
    lll[0] = arrx[lenx-1]; lll[lenx-1] = arrx[0]
    for aa in range(factorx):
        for ddd in range(1, lenx-2):
            avg = arrx[ddd-1] + arrx[ddd] + arrx[ddd+1]
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

# EOF