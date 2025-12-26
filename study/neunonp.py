#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math, sys, argparse

from neuutil import *
from pgutil import *

import numpy as np

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

        self.inputs  = []; self.outputs = []
        self.strength = 0
        for aa in range(inputs):
            #self.inputs.append(neurand())
            self.inputs.append(0.)

        for aa in range(outputs):
            self.outputs.append(0.)

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

    # --------------------------------------------------------------------
    # Fire one neuron. Find smallest diff.

    def fire(self, ins, stride=1):
        #print("fire", ins[:12])
        old = 0xffff ; ooo = []; sss = 0
        for aa in self.trarr:
            #print("firex",  aa[0][:12], end = "\n")
            ss = self.cmp(ins, aa[0], aa[2], stride)
            if old > ss:
                old = ss
                ooo = aa[1]
                sss = ss

        self.outputs = ooo
        self.strength = sss
        return ooo

    def fire_one(self, offs, ins, stride):

        #print("fire_one", ins[:12])
        ss = self.cmp(ins, self.trarr[offs][0], self.trarr[offs][2], stride)
        self.outputs = self.trarr[offs][1]
        self.strength = ss
        return self.trarr[offs][1]

    def __str__(self):
        return "in: " + str(self.inputs)[:20]  + " ... out: " + \
                    str(self.outputs)[:20] + " ..."

    def dump(self):
        for aa in self.trarr:
           print(aa)

    def train(self, ins, outs, step = 1):
        #print(ins, outs)
        self.trarr.append((ins, outs, step))

    def showtrain(self):
        for aa in self.trarr:
            print(aa)

def testneu(nnn, tin, tout):
    tttt = 0
    for aa in range(len(tin)):
        ttt = time.time()
        nnn.fire(tin[aa])
        tttt +=  time.time() - ttt
        print("in", tin[aa][:12], "out",  nnn.outputs,)

        #        "exp",  tout[aa],
        #          "err",  "%.3f" % nnn.strength)
    print("%.3f ms" % (tttt * 1000))

VAL  = 0.5
VAL2 = 0.6

parser = argparse.ArgumentParser(
                    prog='neunonp',
                    description='numpy less neural demo',
                    epilog='')

parser.add_argument('-c', '--count', default=2, type=int)


def test_one(in_arrx, ou_arrx):

    in_arr = []
    for cc in in_arrx:
        in_comp =  [0 for aa in range(args.count)]
        in_arr.append(list(cc) + in_comp)

    #print(in_arr)
    #sys.exit(0)

    nn = NeuNp(len(in_arr), 1)
    print("neunp AND")

    for aa in range(len(in_arr)):
        nn.train(in_arr[aa], ou_arrx[aa])

    #print(nn)
    #nn.dump()

    testneu(nn, in_arr, ou_arr)


if __name__ == '__main__':

    args = parser.parse_args()
    #print("count =", args.count)

    # -----------------------------------------------------------
    # imitate AND gate

    in_arrt =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    ou_arr =  (0, 0, 0, VAL)

    tin_arr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_arr =  (0, 0, 0, VAL)
    test_one(in_arrt, ou_arr)

    #sys.exit(0)

    # -----------------------------------------------------------
    # imitate OR gate

    in_oarrt =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    ou_oarr =  (0, VAL, VAL, VAL,)

    tin_oarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tou_oarr =  (0, VAL, VAL, VAL,)
    test_one(in_oarrt, ou_oarr)

# EOF
