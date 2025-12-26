#!/usr/bin/env python

# ------------------------------------------------------------------------
# NEULUT: Neural Lookup Tables

import random, math, sys

VERBOSE = 0
PGDEBUG = 1
QUADRATIC = 0
# Help identify a neuron by serial number

gl_serial = 0

from pgutil import *

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

        self.strength = 0.
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

    def _cmp(self, ins, ref, step = 1, stride = 1, quad = 0):

        '''  Compare arrays, return sum of mismatch value.
             Obey step value. The flag QUADRATIC will use
             the squre function.
        '''
        #print("cmp", ins, ref, "step:", step, "stirde:", stride)
        ddd = []; res2 = 0.
        prog = 0; prog2 = 0
        try:
            while True:
                if prog2 >= len(ins):
                    break
                if prog >= len(ref):
                    break
                if quad:
                    diff = sqr(ins[prog2] - ref[prog])
                else:
                    diff = ins[prog2] - ref[prog]
                #print("diff", diff)
                ddd.append(diff)
                prog  +=  step
                prog2 +=  stride

        except IndexError:
            #print(sys.exc_info())
            print_exception("cmp idx")
            #raise
            pass
        except:
            #print("cmp", sys.exc_info())
            print_exception("cmp")
            #raise
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

if __name__ == '__main__':

    import neuutil

    VAL   = 1. ;  VAL2  = 0.51 ; OUT   = 1.
    in_arr  =  ( (0, 0), (VAL, 0),  (0, VAL),  (VAL, VAL) )
    tin_arr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    XOR, OR, AND, NAND, NOR = range(5)

    nn = NeuLut(5, 1)

    def tobits(val, lenx):
        ''' Convert number to digital bits '''
        arrx = []
        for aa in range(lenx-1, -1, -1):
            if val & 1 << aa: boolx = 1
            else: boolx = 0
            arrx.append(boolx)
        return arrx
    #for aa in range(5):
    #    print(aa, ":", tobits(aa, 3))
    def train(kindN, in_arr, out_arr, nn):
        kkk = tobits(kindN, 4)
        for aa in range(len(in_arr)):
            inarr = kkk + list(in_arr[aa])
            nn.memorize(inarr, out_arr[aa])

    def testx(kind, kindN, in_arr, out_arr, tin_arr, tout_arr, nn):
        #print("NeuLut %s:" % kind, kindN, kkk, nn)
        kkk = tobits(kindN, 4)
        for aa in range(len(tin_arr)):
            inarr = kkk + list(in_arr[aa])
            nn.fire(inarr, 1)
            print("%-5s" % kind, "in:", tin_arr[aa], "out:", nn.outputs,  end = " ")
            print("expect:", tout_arr[aa], end = " ")
            print(neuutil.is_ok(nn.outputs,  tout_arr[aa]))

    # imitate the AND gate
    out_aarr =  (0, 0, 0, VAL)
    tout_aarr =  (0, 0, 0, VAL)
    train(AND, in_arr, out_aarr, nn)

    # imitate the OR gate
    out_oarr =  (0, OUT, OUT, OUT,)
    tout_oarr =  (0, VAL, VAL, VAL,)
    train(OR, in_arr, out_oarr, nn)

    # imitate the XOR gate
    out_xoarr =  (0, OUT, OUT, 0, )
    tout_xoarr =  (0, OUT, OUT, 0, )
    train(XOR, in_arr, out_xoarr, nn)

    # imitate the NAND gate
    out_narr =  (0, OUT, OUT, OUT, )
    tout_narr =  (0, OUT, OUT, OUT, )
    train(NAND, in_arr, out_narr, nn)

    # imitate the NOR gate
    out_norr =  (OUT, 0, 0, 0, )
    tout_norr =  (OUT, 0, 0, 0)
    train(NOR, in_arr, out_norr, nn)

    #print("Cummulative test:")
    testx("OR:", OR,  in_arr, out_oarr, tin_arr, tout_oarr, nn)
    testx("AND:", AND, in_arr, out_aarr, tin_arr, tout_aarr, nn)
    testx("XOR:", XOR, in_arr, out_xoarr, tin_arr, tout_xoarr, nn)
    testx("NAND:", NAND,in_arr, out_narr, tin_arr, tout_narr, nn)
    testx("NOR:",  NOR, in_arr, out_norr, tin_arr, tout_norr, nn)

# EOF
