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

    cccc = []
    ccc  = load_font_img("letter_a.png")
    ccc2 = load_font_img("letter_b.png")
    ccc3 = load_font_img("letter_c.png")

    cccc.append(ccc)
    cccc.append(ccc2)
    cccc.append(ccc3)

    #print("ccc3", ccc3)
    #print("ccc2", ccc2)
    #print("ccc", ccc)

    #ccc.show()
    #ccc2.show()
    #ccc3.show()
    #sys.exit()

    nn = neulut.NeuLut(ccc.size[0] * ccc.size[1], 2)

    #print("nn", nn, nn.inlen())


     #arrz = newarr(ccc.size[0] * ccc.size[1], 0)
    #nn.train(arrz, ("1",), ccc.size[0])

    #arrf = newarr(ccc.size[0] * ccc.size[1], 255)
    #nn.train(arrf, ("0",), ccc.size[0])

    for xxx in range(len(cccc)):
        nn.train(list(cccc[xxx].getdata()),  (xxx,), cccc[xxx].size[0])

    #print("tr", nn.showtrain())
    #sys.exit()
    #aaa.show()

    bw = load_bw_image("srect_white_abc.png")
    arr3 = bw.getdata()

    # All pixels
    for aa in range(0, bw.size[1], 1):
        for bb in range(0, bw.size[0], 1):

            #bw.putpixel((bb, aa,), ( 100, ))
            #print("box", (aa * 10, bb,)  )
            #sumx.paste(bw, box=(aa * 12, bb * 10,)  )
            #print("arr4", aa, bb, arr4)

            try:
                #fff = nn.fire(arr4, ccc.size[0])
                for ddd in range(len(cccc)):
                    arr4 = []
                    for aaa in range(cccc[ddd].size[1]):
                        for bbb in range(cccc[ddd].size[0]):
                            try:
                                idx = (aa + aaa) * bw.size[0] + (bb + bbb)
                                arr4.append(arr3[idx])

                            except IndexError:
                                arr4.append(200)
                                pass
                            except:
                                print(sys.exc_info())
                                pass

                    #print("ddd", ddd)
                    fff = nn.fire_one(ddd, arr4, cccc[ddd].size[0])
                    if fff[0] !=  ("0") and nn.strength < 15000: #fff[0] !=  ("1"):
                        print(fff, aa, bb,
                                    #"%.3f" % (idx / bw.size[0]), \
                                    #x %.3f" % (idx % bw.size[0]),
                                    "%.3f" % nn.strength, end = "\n")

                    if  ddd == 0:
                        try:
                            bw2 = Image.new("L", (cccc[ddd].size[0],
                                            cccc[ddd].size[1]), color=200 )
                            bw2.putdata(arr4)
                            sumx.paste(bw2, (bb*(cccc[ddd].size[0]+1),
                                        aa*(cccc[ddd].size[1]+1)))

                        except IndexError:
                            print(sys.exc_info())
                            pass
                        except:
                            print(sys.exc_info())
                            pass

            except IndexError:
                #print(sys.exc_info())
                pass
            except:
                print(sys.exc_info())
                print_exception("ff")
                pass

    #bw.show()
    #ccc.show()
    #ccc2.show()
    #ccc3.show()
    sumx.show()

# EOF
