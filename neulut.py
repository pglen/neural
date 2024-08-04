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

    def train(self, ins, outs, step = 1):
        #print(ins, outs)
        self.trarr.append(ins)
        self.resarr.append(outs)

    def showtrain(self):
        for aa in self.trarr:
            print(aa)

#@measure
def testx(kind, in_arr, out_arr, tin_arr, tout_arr):

    nn = NeuLut(2, 1)
    #print("NeuLut %s:" % kind, nn)

    for aa in range(len(in_arr)):
        nn.train(in_arr[aa], out_arr[aa])

    #nn.dump()
    #sys.exit(0)

    for aa in range(len(tin_arr)):
        nn.fire(tin_arr[aa], 1)
        print(kind, "in:", tin_arr[aa], "out:",
                nn.outputs, "expect:", tout_arr[aa], end = " ")
        print(is_ok(nn.outputs,  tout_arr[aa]), end = "")
        print()

''' The generalzation comes from the lattitude of the compare. For
instance, using less than 0.5 for VAL2, the logic interprets it as zero, using
greater than 0.5, the interpreetation is one.
'''

VAL  = 1.
VAL2 = 0.501
OUT = 1.

if __name__ == '__main__':

    # imitate the AND gate

    in_arr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_arr =  (0, 0, 0, OUT)
    tin_arr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_arr =  (0, 0, 0, OUT)

    #ttt = time.time()
    testx("AND ", in_arr, out_arr, tin_arr, tout_arr)
    #print("Exe: %.3f us" % ((time.time() - ttt) * 1000000))

    # -----------------------------------------------------------
    # imitate the OR gate

    in_oarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_oarr =  (0, OUT, OUT, OUT,)
    tin_oarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_oarr =  (0, VAL, VAL, VAL,)

    testx("OR  ", in_oarr, out_oarr, tin_oarr, tout_oarr)

    # -----------------------------------------------------------
    # imitate the XOR gate

    in_xarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_xarr =  (0, OUT, OUT, 0, )
    tin_xarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_xarr =  (0, OUT, OUT, 0, )

    testx("XOR ", in_xarr, out_xarr, tin_xarr, tout_xarr)

    # -----------------------------------------------------------
    # imitate the NAND gate

    in_xarr =  ( (0, 0), (VAL, 0), (0, VAL), (VAL, VAL) )
    out_xarr =  (0, OUT, OUT, OUT, )
    tin_xarr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
    tout_xarr =  (0, OUT, OUT, OUT, )

    testx("NAND", in_xarr, out_xarr, tin_xarr, tout_xarr)

# EOF
