#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math, sys

from neuutil import *
from pgutil import *

VERBOSE = 0
PGDEBUG = 1
QUADRATIC = 0
# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------

class NeuLut():

    '''     The basic building block of neural lookup table.
            The training material is pushed to an array;
            The lookup is executed finding the closest match.
    '''

    def __init__(self, inputs, outputs):

        global gl_serial

        # These are helpers
        self.serial = gl_serial; gl_serial += 1;

        if VERBOSE:
            print("NeuLut init ",  "inuts %.03f " % inputs) #, end=' ')

        self.inputs  = []; self.outputs = []; self.trarr = []

        # Alloc, provide defaults
        for aa in range(inputs):
            self.inputs.append(0.)

        for aa in range(outputs):
            self.outputs.append(0.)

        self.trarr = []; self.resarr = []

    def inlen(self):
        return len(self.inputs)

    def outlen(self):
        return len(self.outputs)

    def _cmp(self, ins, ref, step = 1, stride = 1):

        '''  Compare arrays, return sum of mismatch value.
             Obey step value. The flag QUADRATIC will use
             the squre function.
        '''
        #print("cmp", ins, val, "step", step, "strde", stride)
        ddd = []; res2 = 0.
        prog = 0; prog2 = 0
        try:
            while True:
                if prog2 >= len(ins):
                    break
                if prog >= len(ref):
                    break
                #diff = sqr(ins[prog2] - ref[prog])
                diff = ins[prog2] - ref[prog]
                #print("diff", diff)
                ddd.append(diff)
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
            res2 += abs(bb)
            #res2 += bb

        if len(ddd):
            return res2 / len(ddd)
        else:
            return 0

    def fire_one(self, offs, ins, stride):

        #print("fire_one", ins[:12])
        ss = self._cmp(ins, self.trarr[offs][0], self.trarr[offs][2], stride)
        self.outputs = self.trarr[offs][1]
        self.strength = ss
        return self.trarr[offs][1]

    # --------------------------------------------------------------------
    def fire(self, ins, stride):

        ''' Fire one neuron. Sum all diffs, div by count. '''

        #print("fire", ins[:12])
        old = 0xffff; idx = -1; sss = 0
        #print("  ins", ins)
        for aa in range(len(self.trarr)):
            ref = self.trarr[aa]
            ss = self._cmp(ins, ref, stride)
            #print("   train:", ref, "diff:", ss)
            if old > ss:
                old = ss
                idx = aa
        self.outputs = self.resarr[idx]
        return self.outputs

    def __str__(self):
        return "ins: " + str(self.inputs)[:20]  + " outs: " + \
                    str(self.outputs)[:20]

    def dump(self):
        for cnt, aa in enumerate(self.trarr):
            arr2 = rle(aa)
            print("%-2d" % cnt,  self.resarr[cnt], arr2[:6], "...")

    def memorize(self, ins, outs, step = 1):
        #print(ins, outs)
        self.trarr.append(ins)
        self.resarr.append(outs)

    def showtrain(self):
        for aa in self.trarr:
            print(aa)

''' The generalzation comes from the lattitude of the compare. For
instance, using less than 0.5 for VAL2, the logic interprets it as zero,
using greater than 0.5, the interpreetation is one.
'''

# ------------------------------------------------------------------------
# Tests

XOR, OR, AND, NAND, NOR = range(5)

def tobits(val, lenx):
    arrx = []
    for aa in range(lenx-1, -1, -1):
        if val & 1 << aa: boolx = 1
        else: boolx = 0
        #print("bit %d:" % aa, boolx, end = " ")
        arrx.append(boolx)
    #print()
    return arrx

#print(tobits(OR, 3))
#print(tobits(XOR, 3))
#print(tobits(AND, 3))
#print(tobits(NAND, 3))
#print(tobits(NOR, 3))

def train(kindN, in_arr, out_arr, nn):
    kkk = tobits(kindN, 4)
    for aa in range(len(in_arr)):
        inarr = kkk + list(in_arr[aa])
        nn.memorize(inarr, out_arr[aa])

def testx(kind, kindN, in_arr, out_arr, tin_arr, tout_arr, nn):

    #print("NeuLut %s:" % kind, kindN, kkk, nn)
    #nn.dump()
    kkk = tobits(kindN, 4)
    for aa in range(len(tin_arr)):
        inarr = kkk + list(in_arr[aa])
        nn.fire(inarr, 1)
        print(kind, "in:", tin_arr[aa], "out:",
                nn.outputs, "expect:", tout_arr[aa], end = " ")
        print(is_ok(nn.outputs,  tout_arr[aa]), end = "")
        print()

VAL  = 1.
VAL2 = 0.501
OUT = 1.

if __name__ == '__main__':

    nn = NeuLut(4, 1)

    # imitate the AND gate

    in_aarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_aarr =  (0, 0, 0, OUT)
    tin_aarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_aarr =  (0, 0, 0, OUT)

    #ttt = time.time()
    train(AND, in_aarr, out_aarr, nn)
    #testx("AND ", AND, in_aarr, out_aarr, tin_aarr, tout_aarr, nn)
    #print("Exe: %.3f us" % ((time.time() - ttt) * 1000000))

    # -----------------------------------------------------------
    # imitate the OR gate

    in_oarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_oarr =  (0, OUT, OUT, OUT,)
    tin_oarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_oarr =  (0, VAL, VAL, VAL,)

    train(OR, in_oarr, out_oarr, nn)
    #testx("OR  ", OR, in_oarr, out_oarr, tin_oarr, tout_oarr, nn)

    # -----------------------------------------------------------
    # imitate the XOR gate

    in_xoarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL))
    out_xoarr =  (0, OUT, OUT, 0, )
    tin_xoarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_xoarr =  (0, OUT, OUT, 0, )

    train(XOR, in_xoarr, out_xoarr, nn)
    #testx("XOR ", XOR, in_xoarr, out_xoarr, tin_xoarr, tout_xoarr, nn)

    # -----------------------------------------------------------
    # imitate the NAND gate

    in_narr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_narr =  (0, OUT, OUT, OUT, )
    tin_narr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_narr =  (0, OUT, OUT, OUT, )

    train(NAND, in_narr, out_narr, nn)
    #testx("NAND", NAND, in_narr, out_narr, tin_narr, tout_narr, nn)

    # -----------------------------------------------------------
    # imitate the NOR gate

    in_norr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_norr =  (OUT, 0, 0, 0, )
    tin_norr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_norr =  (OUT, 0, 0, 0)

    train(NOR, in_norr, out_norr, nn)
    #testx("NOR", NOR, in_norr, out_norr, tin_norr, tout_norr, nn)

    # Cummulative test
    print("Cummulative test:")
    testx("OR  ", OR, in_oarr, out_oarr, tin_oarr, tout_oarr, nn)
    testx("AND ", AND, in_aarr, out_aarr, tin_aarr, tout_aarr, nn)
    testx("XOR ", XOR, in_xoarr, out_xoarr, tin_xoarr, tout_xoarr, nn)
    testx("NAND", NAND, in_narr, out_narr, tin_narr, tout_narr, nn)
    testx("NOR", NOR, in_norr, out_norr, tin_norr, tout_norr, nn)

# EOF
