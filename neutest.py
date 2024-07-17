#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import sys, random, math

from PIL import Image

#import trans, tenticle, neuutil

from neuutil import *
from pgutil import *
import neulut

verbose = 0


if __name__ == '__main__':

    sumx = Image.new("L", (800,600), color=(100) )

    ccc3 = load_font_img("letter_b.png")
    ccc2  = load_font_img("letter_a.png")
    ccc = load_font_img("letter_c.png")
    print("ccc3", ccc3)
    print("ccc2", ccc2)
    print("ccc", ccc)

    #ccc.show()
    #ccc2.show()
    #ccc3.show()
    #sys.exit()

    nn = neulut.NeuLut(ccc.size[0] * ccc.size[1], 2)

    #print("nn", nn, nn.inlen())

    arrz = newarr(ccc.size[0] * ccc.size[1], 0)
    nn.train(arrz, ("1",), ccc.size[0])

    arrf = newarr(ccc.size[0] * ccc.size[1], 255)
    nn.train(arrf, ("0",), ccc.size[0])

    nn.train(list(ccc.getdata()),  ("b",), ccc.size[0])
    nn.train(list(ccc2.getdata()), ("a",), ccc2.size[0])
    nn.train(list(ccc3.getdata()), ("c",), ccc3.size[0])

    #print("tr", nn.showtrain())
    #sys.exit()
    #aaa.show()

    bw = load_bw_image("srect_white_abc.png")
    arr3 = bw.getdata()

    for aa in range(0, bw.size[1], 2):

        #print()

        for bb in range(0, bw.size[0], 2):
            #bw.putpixel((bb, aa,), ( 100, ))

            #print("box", (aa * 10, bb,)  )
            #sumx.paste(bw, box=(aa * 12, bb * 10,)  )

            arr4 = []

            for aaa in range(ccc.size[1]):
                for bbb in range(ccc.size[0]):
                    try:
                        idx = (aa + aaa) * bw.size[0] + (bb + bbb)
                        arr4.append(arr3[idx])

                    except IndexError:
                        pass
                    except:
                        print(sys.exc_info())
                        pass

            #print("arr4", aa, bb, arr4)

            try:
                fff = nn.fire(arr4, ccc.size[0])
                if fff[0] !=  ("0"): # and fff[0] !=  ("1"):
                    print(fff, idx, aa, bb,
                                #"%.3f" % (idx / bw.size[0]), \
                                #x %.3f" % (idx % bw.size[0]),
                                "%.3f" % nn.strength, end = "\n")
            except IndexError:
                #print(sys.exc_info())
                pass
            except:
                print(sys.exc_info())
                print_exception("ff")
                pass

            try:
                bw2 = Image.new("L", (ccc.size[0], ccc.size[1]), color=200 )
                bw2.putdata(arr4)
                sumx.paste(bw2, (bb*8, aa*8,))

            except IndexError:
                print(sys.exc_info())
                pass
            except:
                print(sys.exc_info())
                pass

    #bw.show()
    #ccc.show()
    #ccc2.show()
    #ccc3.show()
    sumx.show()


# EOF


