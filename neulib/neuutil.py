#!/usr/bin/env python

import os, sys, random, time
from PIL import Image, ImageFont, ImageDraw

ddd = os.path.dirname(__file__)
if ddd not in sys.path:
    sys.path.append(ddd)

from pgdict import *

def pn(num):
    return "% -7.3f" % num

def randmemb(var):

    ''' Deliver a random member of an array '''

    if type(var) != type(()) and type(var) != type([]) :
        raise ValueError("Must be a list / array")
    rnd = random.randint(0, len(var)-1)
    #print "randmemb", rnd, "of", len(var)-1
    return var[rnd];

def neurand():

    ''' Deliver a random number in range of 0 to +1 '''

    ret = random.random();
    #print "%+0.3f " % ret,
    return ret

def neurand2():

    ''' Deliver a random number in range of -1 to +1 '''

    ret = random.random() * 2 - 1;
    #print("neurand %+0.3f " % ret)
    return ret

def sqr(vvv):
    ''' return square of number '''
    return vvv * vvv

def parr(arr):
    ''' print array '''
    for aa in arr:
        print(pn(aa), end = " ")
    print()

def print_is_ok(val, ref):
    ''' output terminal string '''
    if val == ref:
        ret = "\033[32;1mOK\033[0m"
    else:
        ret = "\033[31;1mERR\033[0m"
    return ret

def newarr(size, fill):
    ''' Create array with size and fill '''
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
    '''   '''
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

def raisededges(arrx, size):

    ''' detect raising  edges '''

    lenx = len(arrx) ; prev = 255
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if prev < arrx[ddd]:
            eee[ddd] = True
        prev = arrx[ddd]
    return eee

def falledges(arrx, size):

    ''' detect falling edges '''

    lenx = len(arrx) ; prev = 255
    eee = [0 for _ in range(lenx) ]
    for ddd in range(lenx):
        if prev > arrx[ddd]:
            eee[ddd] = True
        prev = arrx[ddd]
    return eee

def vraisededges(arrx, size):

    ''' detect vertical raising  edges '''

    lenx = len(arrx)
    eee = [0 for _ in range(lenx) ]
    for aa in range(size[0]):
        prev = 255
        for bb in range(size[1]):
            ddd = aa + size[0] * bb
            if prev > arrx[ddd]:
                eee[ddd] = True
            prev = arrx[ddd]
    return eee

def vfalledges(arrx, size):

    ''' detect vertical falling edges '''

    lenx = len(arrx)
    eee = [0 for _ in range(lenx) ]
    for aa in range(size[0]):
        prev = 255
        for bb in range(size[1]):
            ddd = aa + size[0] * bb
            if prev < arrx[ddd]:
                eee[ddd] = True
            prev = arrx[ddd]
    return eee

def crossfunc(arr1, arr2):
    lenx = len(arr1)
    eee = [0 for _ in range(lenx) ]
    for idx in range(lenx):
        #print(arr1[idx], arr2[idx], end = "  ")
        if arr1[idx] and arr2[idx]:
            eee[idx] = True
    return eee

def sections(thh1x, thh2y, bww, ppp = None):

    ''' Boundary by non zero sectons

          Parameters:
                    thh1x (arr):    zero crossings x dim
                    thh2y (arr):    zero crossings y dim
                    bww (Image):    image for debug output
                    ppp (Image):    image for debug output

            Returns:
                    DeepDict array of renderable
    '''

    ret = DeepDict()

    prog = 0; xlen = len(thh2y); curr = 0
    while True:
        if prog >=  xlen:
            break
        if thh2y[prog]:
            while True:
                if prog >=  xlen:
                    break
                if  not thh2y[prog]:
                    #print()
                    break
                # one X section
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
                if ppp:
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

    arr2 = []
    if not len(arr):
        return arr2
    prev = arr[0]; cntx = 1
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
    # Special case: all the same values
    if cntx > 1:
        arr2.append((cntx-1, prev))
    return arr2

def scale(lettx, newx, newy, ppp = None):

    #print(lettx)
    rows = [] ; cols = []
    for nx, ny, val in lettx:
        if nx not in cols:
            cols.append(nx)
        if ny not in rows:
            rows.append(ny)
    aspx =  newx /len(cols)   ; aspy =   newy / len(rows)
    #print("aspx %.3f" % aspx, "aspy %.3f" % aspy, "new:",
    #                newx, "old", len(cols), newy, len(rows))
    #ret = []
    retx = ret = DeepDict()
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
            #ret.append((aa, bb, val))
            retx[aa][bb] = val
    if ppp:
        pass
        #for aa, bb, val in ret:
        #    ppp.putpixel((aa, bb), val)
        #    pass
    #print(len(ret))
    return ret

def genfonts(neu, fnamex, lettersx, sumx = None):

    '''
        neu:        neulut
        fnamex      name of font
        lettersx    list of letters
        sumx        debug image to dump fonts to
    '''

    font = ImageFont.truetype(fnamex, 20)
    if sumx:
        sumbox = sumx.getbbox()
        ypos = 10 ;  xpos = 10
    for aa in lettersx:
        sss = font.getbbox(aa)
        #print("letter:", aa, sss, end = "  ")
        fff = Image.new("L", sss[2:], color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)
        ddd = list(fff.getdata())
        neu.memorize(ddd, aa)
        if sumx:
            sumx.paste(fff, (xpos, ypos,))
            xpos += sss[2] + 4
            if xpos > sumbox[2] - 15:
                xpos = 10 ; ypos += 20
        #print("ddd:", len(ddd), ddd)
    return neu

class CustomArrayObject:
    def __init__(self, data_list):
        # Use Python's built-in array module for memory management
        self.data = array.array('B', data_list)
        self.shape = (len(data_list),)
        self.typestr = '|B' # '|d' for double (8-byte float)

    @property
    def __array_interface__(self):
        # Get the pointer to the underlying C data buffer
        data_ptr = self.data.buffer_info()[0]
        return {
            'shape': self.shape,
            'typestr': self.typestr,
            'data': (data_ptr, False), # Pointer and read-only flag (False for writeable)
            'version': 3 # Optional: interface version
        }

# EOF
