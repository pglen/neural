#!/usr/bin/env python3

# ------------------------------------------------------------------------
# Neural network test

'''
   Test cases for simple gates with diverging values
'''

import random, math, sys, argparse

from neuutil import *
from pgutil import *

import numpy as np

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------
# The basic building block, numpy implementation
# The training material is pushed to an array;
# The lookup is executed finding the closest match

class NeuNp():

    def __init__(self, inputs, outputs):

        global gl_serial

        # These are helpers
        self.serial = gl_serial; gl_serial += 1;
        if verbose:
            print("neulut init ",  "inuts %.03f " % inputs) #, end=' ')

        self.inputs  = np.zeros(inputs)
        self.ouputs  = np.zeros(outputs)
        self.trarr = []

    def inlen(self):
        return len(self.inputs)

    # --------------------------------------------------------------------
    # Compare arrays, return closest match value

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
            ss = self.cmp2(ins, aa[0])
            #print(ss)
            if old > ss:
                old = ss
                ooo = aa[1]

        self.outputs = ooo
        return ooo

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):
        for aa in self.trarr:
           print(aa)

    def train(self, ins, outs, step = 1):
        #print(ins, outs)
        self.trarr.append((np.array(ins), outs, step))

def testneu(nnn, tin, tout):
    tttt = 0
    for cnt, aa in enumerate(tin):
        ttt = time.time()
        nnn.fire(aa)
        tttt +=  time.time() - ttt
        print("in", aa[:12], "out",  nnn.outputs, is_ok(nnn.outputs, tout[cnt]))
    print("%.3f ms" % (tttt * 1000) )

VAL  = 0.5
VAL2 = 0.6

arr_0 =  (0,0)
arr_1 =  (0,VAL)
arr_2 =  (VAL,0)
arr_3 =  (VAL,VAL)

def test_train_check(in_arrx, ou_arrx,  tin_arrx, tou_arrx):

    in_arr = []; tin_arr = []
    for cnt, cc in enumerate(in_arrx):
        in_comp =  [0 for aa in range(args.count)]
        in_arr.append(list(cc) + in_comp)
        tin_arr.append(list(tin_arrx[cnt]) + in_comp)
    #print(in_arr)
    nn = NeuNp(len(in_arr), 1)
    for aa in range(len(in_arr)):
        nn.train(in_arr[aa], ou_arrx[aa])
    testneu(nn, tin_arr, tou_arrx)


parser = argparse.ArgumentParser(
                    prog='neunp',
                    description='neural demo',
                    epilog='')
parser.add_argument('-c', '--count', default=2, type=int)

if __name__ == '__main__':

    args = parser.parse_args()

    # imitate the AND gate
    in_andarr =  (arr_0, arr_1,  arr_2,  arr_3,)
    ou_andarr =  (0, 0, 0, 1)
    tin_andarr =  ((0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_andarr =  (0, 0, 0, 1)

    print("NeuNp AND:")
    test_train_check(in_andarr, ou_andarr, tin_andarr, tou_andarr)

    # imitate the OR gate
    in_orarr =  (arr_0, arr_1,  arr_2,  arr_3, )
    ou_orarr =  (0, 1, 1, 1,)
    tin_orarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_orarr =  (0, 1, 1, 1,)

    print("NeuNp OR:")
    test_train_check(in_orarr, ou_orarr, tin_orarr, tou_orarr)

# EOF
