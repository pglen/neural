#!/usr/bin/env python

''' Neural network test '''

import sys, random, math
from PIL import Image

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut
#neulut.VERBOSE = 2

from Crypto import Random
import secrets

if __name__ == '__main__':

    sumx = Image.new("L", (800,600), color=(100) )

    #rrr = Random.get_random_bytes(1)
    #print(dir())
    #secure_bits = secrets.randbits(8)
    #print(secure_bits)
    #sys.exit(0)

    #for aa in range(sumx.size[1]):
    #    for bb in range(sumx.size[0]):
    #        if aa < sumx.size[1] / 3:
    #            sumx.putpixel((bb, aa), int(random.random() * 256))
    #        elif aa < 10*3 * sumx.size[1] / (10 * 3):
    #            sumx.putpixel((bb, aa), 0)
    #            pass
    #        else:
    #            sumx.putpixel((bb, aa), (secrets.randbits(32) >> 16) % 256)

    ccc3 = load_font_img("png/letter_b.png")
    ccc2  = load_font_img("png/letter_a.png")
    ccc = load_font_img("png/letter_c.png")
    #print("ccc3", ccc3)
    #print("ccc2", ccc2)
    #print("ccc", ccc, ccc.size)
    #sys.exit(0)

    sumf = Image.new("L", (400,300), color=(100) )
    sumf.paste(ccc, (2, 2))
    sumf.paste(ccc3, (20, 2))
    sumf.paste(ccc2, (40, 2))
    #sumf.show()
    #sys.exit()
    sumx.paste(sumf, (10, 450))
    nn = neulut.NeuLut()

    #print("nn", nn, nn.inlen())
    #arrz = newarr(ccc.size[0] * ccc.size[1], 0)
    #nn.memorize(arrz, ("c",), ccc.size[0])
    #arrf = newarr(ccc.size[0] * ccc.size[1], 255)
    #nn.memorize(arrf, ("0",), ccc.size[0])

    fl = len(list(ccc.getdata()))

    # All white and all black
    nn.memorize([ 0 for nn in range(fl) ],  (" ",))
    nn.memorize([ 255 for nn in range(fl) ],  ("-",))

    nn.memorize(list(ccc.getdata()),  ("b",))
    nn.memorize(list(ccc2.getdata()), ("a",))
    nn.memorize(list(ccc3.getdata()), ("c",))

    #print("tr", nn.showtrain())
    #ccc.show()
    #sys.exit()
    bw = load_bw_image("png/srect_white_abc.png")
    sumx.paste(bw, (10, 500))
    arr3 = list(bw.getdata())
    #print("bw:", bw, "len arr3:", len(arr3))
    for aa in range(0, bw.size[1], 1):
        #print()
        for bb in range(0, bw.size[0]-8, 1):
            try:
                idx = + aa * bw.size[0] + bb
                bw.putpixel((bb, aa), int(random.random()*255))
                #print(aa, bb, "idx:", idx)
                fff = nn.recall(arr3[idx:], bw.size[0])
                if fff[0] != ("-"): # and fff[0] !=  (" "):
                    print(fff, aa, bb,
                                #"%.3f" % (idx / bw.size[0]), \
                                #x %.3f" % (idx % bw.size[0]),
                                "dev, %.3f" % nn.deviation, end = "\n")
            except IndexError:
                #print(sys.exc_info())
                pass
            except:
                print(sys.exc_info())
                print_exception("ff")
                pass
            try:
                #bw2 = Image.new("L", (ccc.size[0], ccc.size[1]), color=200 )
                #bw2.putdata(arr4)
                #sumx.paste(bw2, (bb*8, aa*8,))
                pass
            except IndexError:
                print(sys.exc_info())
                pass
            except:
                print(sys.exc_info())
                pass

    sumx.paste(bw, (120, 500))

    sumx.show()

# EOF
