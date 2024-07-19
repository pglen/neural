#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math, sys

from neuutil import *
from pgutil import *

import numpy as np
#from numba import njit

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------
# The basic building block
# The training material is pushed to an array;
# The lookup is executed finding the closest match

class NeuNp():

    def __init__(self, inputs, outputs):

        global gl_serial

        # These are helpers
        self.serial = gl_serial; gl_serial += 1;

        if verbose:
            print("neulut init ",  "inuts %.03f " % inputs) #, end=' ')

        #self.inputs  = []; self.outputs = []
        self.strength = 0

        self.inputs  = np.zeros(inputs)
        self.ouputs  = np.zeros(outputs)
        self.trarr = []

    def inlen(self):
        return len(self.inputs)

 
    # --------------------------------------------------------------------
    # Compare arrays, return largest mismatch value
    # Obey step value

    def cmp(self, ins, val, step, stride):

        #print("cmp", ins, val, "step", step, "strde", stride)

        ddd = []; res2 = 0.
        prog = 0; prog2 = 0
        try:
            while True:

                if prog2 >= len(ins):
                    break

                for aa in range(step):
                    #print("ooo", aa, org[aa], val[aa], end=" ")
                    ddd.append(sqr(ins[prog2 + aa] - val[prog + aa]))
                prog  +=  step
                prog2 +=  stride

        except IndexError:
            #print(sys.exc_info())
            pass
        except:
            #print("cmp", sys.exc_info())
            print_exception("cmp")
            pass

        #print("ddd", end = " "); parr(ddd)
        for bb in ddd:
            #res2 = math.sqrt(sqr(bb) + sqr(res2))
            res2 += bb

        if len(ddd):
            return res2 / len(ddd)
        else:
            return 0

    def cmp2(self, ins, val):
         #ret = np.power(np.subtract(ins, val),2)
         ret = np.abs(np.subtract(ins, val))
         #print("ins", ins, "val", val, "ret", 
         #           ret, "sum", ret.sum())
         sum = ret.sum()
         #print("cmp2", ins, val, sum)

         return sum

    # --------------------------------------------------------------------
    # Fire one neuron. Find smallest diff.

    def fire(self, ins, stride=1):
        #print("fire", ins[:12])
        old = 0xffff ; ooo = []
        for aa in self.trarr:
            #print("firex",  aa[0][:12], end = "\n")
            #ss = self.cmp(ins, aa[0], aa[2], stride)
            ss = self.cmp2(ins, aa[0])
            #print(ss)
            if old > ss:
                old = ss
                ooo = aa[1]
            #break

        self.outputs = ooo
        self.strength =  old
        return ooo

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):
        for aa in self.trarr:
           print(aa)

    def train(self, ins, outs, step = 1):
        #print(ins, outs)
        self.trarr.append((ins, outs, step))


def testneu(nnn, tin, tout):
    tttt = 0
    for aa in tin:
        ttt = time.time()
        nnn.fire(aa)
        tttt +=  time.time() - ttt
        print("in", aa, "out",  nnn.outputs,)

        #        "exp",  tout[aa],
        #          "err",  "%.3f" % nnn.strength)
    print("%.3f ms" % (tttt * 1000))

VAL  = 0.5
VAL2 = 0.6

arr_0 =  np.array ((0,0))
arr_1 =  np.array ((0,VAL))
arr_2 =  np.array ((VAL,0))
arr_3 =  np.array ((VAL,VAL))

# imitate and gate

in_arr =  (arr_0, arr_1,  arr_2,  arr_3, )
ou_arr =  (0, 0, 0, 1)

tin_arr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
tou_arr =  (0, 0, 0, VAL)

def andgate():
    pass

# imitate or gate

in_oarr =  (arr_0, arr_1,  arr_2,  arr_3, )
ou_oarr =  (0, 1, 1, 1,)

tin_oarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
tou_oarr =  (0, VAL, VAL, VAL,)


if __name__ == '__main__':

    nn = NeuNp(2, 1)
    print("neunp AND")

    for aa in range(len(in_arr)):
        nn.train(in_arr[aa], ou_arr[aa])

    #print(nn)
    #nn.dump()

    testneu(nn, in_arr, ou_arr)
    #sys.exit(0)

    # -----------------------------------------------------------

    nn2 = NeuNp(2, 1)
    print("\nneunp OR")

    for aa in range(len(in_oarr)):
        nn2.train(in_oarr[aa], ou_oarr[aa])

    #print(nn)
    #nn.dump()

    testneu(nn2, in_oarr, ou_oarr)

# EOF