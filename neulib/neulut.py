#!/usr/bin/env python

''' NEULUT: Neural Lookup Tables
    The generalization comes from the latitude of the compare. For
    instance, using less than 0.5 for VAL2, the logic interprets it as zero,
    using greater than 0.5, the interpretation is one.
'''

import random, math, sys

VERBOSE = 0
PGDEBUG = 1
QUADRATIC = 0

# Help identify a neuron by serial number
class gl_serial():
    num = 0

#from pgutil import *

# ------------------------------------------------------------------------

class NeuLut():

    '''     The basic building block of neural lookup table.
            The training material is pushed to an array;
            The lookup is executed finding the closest match.
    '''

    def __init__(self, inputs = [], outputs = []):

        # These are helpers
        self.serial = gl_serial.num; gl_serial.num += 1;

        if VERBOSE:
            print("NeuLut init:",  "inputs %.03f " % inputs) #, end=' ')

        self.strength = 0.
        self.inputs  = []; self.outputs = []; self.trainarr = []
        # Alloc, provide defaults
        for aa in range(inputs):
            self.inputs.append(0.)
        for aa in range(outputs):
            self.outputs.append(0.)
        self.trainarr = []; self.resarr = []

    def memorize(self, ins, outs, step = 1):
        ''' Memorize
              ins       array to remember
              outs      outputs for this input array
        '''
        #print(ins, outs)
        self.trainarr.append(ins)
        self.resarr.append(outs)

    def recall(self, ins, stride = 1):
        ''' Recall from memory. Sum all diffs, div by count.
            input:
                    ins     array to compare to
                    stride  line stride if 2d lines
            out:
                    the remembered sequence
        '''
        old = 0xffff; idx = -1
        #print("  ins", ins)
        for aa in range(len(self.trainarr)):
            ref = self.trainarr[aa]
            ss = self._cmp(ins, ref, stride)
            if old > ss:
                old = ss
                idx = aa
        if VERBOSE:
            print("   recall:", idx, self.resarr[idx])
        self.outputs = self.resarr[idx]
        return self.outputs

    def _cmp(self, ins, ref, step = 1, stride = 1, quad = 0):

        '''  Compare arrays, return sum of mismatch value.
             Obey step value. The flag QUADRATIC will use
             the squre function.
        '''
        if VERBOSE > 1:
            print("    cmp:", ins, ref, end = " ")
            #"step:", step, "stride:", stride)

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
            retx = res2 / len(ddd)
        else:
            retx = 0
        if VERBOSE > 1:
            print("ret = %.2f" % retx)
        return retx

    def __str__(self):
        return "ins: " + str(self.inputs)[:20]  + " outs: " + \
                    str(self.outputs)[:20]

    def dump(self):
        for cnt, aa in enumerate(self.trainarr):
            arr2 = rle(aa)
            print("%-2d" % cnt,  self.resarr[cnt], arr2[:6], "...")

    def showtrain(self):
        for aa in self.trainarr:
            print(aa)
    #def inlen(self):
    #    return len(self.inputs)
    #
    #def outlen(self):
    #    return len(self.outputs)

# EOF
