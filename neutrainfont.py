#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import os, sys, random, math

from PIL import Image, ImageFont, ImageDraw

#import trans, tenticle, neuutil

from neuutil import *

import neulut
import neunp

verbose = 0
imgdir = "png"

letters = [ chr(nn) for nn in range(32, 127) ]
#print(letters)

testx = []

if __name__ == '__main__':

    print("Train fonts")

    #nlut = neulut.NeuLut(200, 8)
    nlut = neunp.NeuNp(200, 8)

    bw = load_bw_image(os.path.join(imgdir, "srect_white_abc.png"))
    print("bw size", bw.size)

    orgx = bytes(bw.getdata())
    #print(orgx[1000:1500])
    #sys.exit(0)

    pp = Image.new(bw.mode, bw.size, color=255)
    ppp = Image.new(bw.mode, bw.size, color=255)
    sumx = Image.new("L", (500,300), color=(150) )

    #font = ImageFont.load_default()
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    #font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf", 20)

    # Flatten font to linear
    row = 10; hhh = 10
    aaa = 0; bbb = 0
    letters = "abcdefgh"
    for aa in letters:
        sss = font.getsize(aa)
        aaa += sss[0]; bbb += sss[1]
    aaa //= len(letters)
    bbb //= len(letters)

    for aa in letters:
        sss = font.getsize(aa)
        fff = Image.new("L", sss, color=(255) )
        draw = ImageDraw.Draw(fff)
        draw.text((0, 0), aa, font=font)
        #scale to uniform
        #fff = fff.resize((sss[0], sss[1]))
        fff = fff.resize((aaa, bbb))

        ddd = list(fff.getdata())
        if aa == 'a':
            testx = ddd[:]
        #print(aa, len(ddd), sss, ddd)
        nlut.train(ddd, aa)
        sumx.paste(fff, (hhh, row,))
        hhh += aaa + 5
        if hhh > 450:
            hhh = 10
            row += 20
        #nlut.dump()

    # Recog. For every coordinate, build input
    for yy in range(0, bw.size[1] - bbb, 1):
        for xx in range(0, bw.size[0] - aaa, 1):
            ins2 = []
            for yyy in range(bbb):
                start = (yyy + yy) * bw.size[0] + xx;
                #print(orgx[start:start+aaa])
                ins2.append(orgx[start:start+aaa])
            ins = list(b"".join(ins2))
            #print(rle(ins))
            if xx == 30 and yy == 10:
                #print("ins2", ins2)
                for yyyy in range(bbb):
                    for xxxx in range(aaa):
                        try:
                            pix = bw.getpixel((xx + xxxx, yy + yyyy))
                            pp.putpixel((xxxx + xx, yyyy + yy), pix // 2)
                            ppp.putpixel((xxxx + xx, yyyy + yy), ins2[yyyy][xxxx])
                        except IndexError:
                            pass
                        except:
                            print(sys.exc_info())

            #ttt = time.time()
            if len(ins) == aaa*bbb:
                res = nlut.fire(ins)
                pass
            else:
                print("bad len", len(ins))

            #print("one cycle: %.3f ms" % ((time.time()-ttt) * 1000) )
            if  nlut.distance != 10149:
                print("coor %2d %2d" % (xx, yy), "res:", nlut.outputs, "dist", nlut.distance)

    # Show                                (
    sumx.paste(bw,  (10, row+40,))
    sumx.paste(pp,  (10, row+100,))
    sumx.paste(ppp, (10, row+160,))
    #sumx.show()

    sumx2 = sumx.resize((sumx.size[0] * 3, sumx.size[1] * 3))
    sumx2.show()

# EOF
