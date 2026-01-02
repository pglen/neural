#!/usr/bin/env python

''' NEULUT: Neural Lookup Tables
    The generalization comes from two factors:

        The latitude of the compare.
        The compare will deliver closest match
    For instance, using less than 0.5 for VAL2, the logic
    interprets it as zero, using greater than 0.5, the interpretation
    is one.
    Another instance, if there is no exact match, the function will
    deliver the closest match. Also, the variable 'deviation' contains
    the sum deviation value.
'''

import os, sys, random #, math

VERBOSE = 0
PGDEBUG = 1
QUADRATIC = 0

ddd = os.path.dirname(__file__)
if ddd not in sys.path:
    sys.path.append(ddd)

from pgutil import *
from neuutil import *

# Help identify a neuron by serial number
class gl_serial():
    num = 0

class NeuLut():

    '''     The basic building block of neural lookup table.
            The training material is pushed to an array;
            The lookup is executed finding the closest match.
    '''

    def __init__(self, inputs = 0, outputs = 0):

        # These are helpers
        self.serial = gl_serial.num; gl_serial.num += 1;

        if VERBOSE:
            print("NeuLut init:",  "inputs %.03f " % inputs) #, end=' ')

        self.deviation = 0.
        self.inputs  = []; self.outputs = []; self.trainarr = []
        # Alloc, provide defaults
        for aa in range(inputs):
            self.inputs.append(0.)
        for aa in range(outputs):
            self.outputs.append(0.)
        self.trainarr = []; self.resarr = []

    def memorize(self, ins, outs):
        ''' Memorize
              ins:       array to remember
              outs:      outputs for this input array
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

        if VERBOSE > 1:
            print("  ins", rle(ins))

        self.deviation = 0xffffffff;
        idx = -1
        for aa in range(len(self.trainarr)):
            ref = self.trainarr[aa]
            ss = self._cmp(ins, ref, 1, stride)
            if self.deviation > ss:
                self.deviation = ss
                idx = aa
        if VERBOSE:
            print("   recall:", idx, self.resarr[idx])
        self.outputs = self.resarr[idx]
        return self.outputs

    def _cmp(self, ins, ref, step, stride):

        '''  Compare arrays, return sum of mismatch value. Obey step
             value. The flag QUADRATIC will use the square function.
        '''
        if VERBOSE > 2:
            print("    cmp:", ins, ref, end = " ")
        ssum = 0 ; prog = 0; prog2 = 0; cnt = 0
        try:
            while True:
                if prog2 >= len(ins):
                    break
                if prog >= len(ref):
                    break
                ssum += abs(ins[prog2] - ref[prog])
                prog  +=  step ;  prog2 +=  stride
                cnt += 1
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
        if cnt:
            retx = ssum / cnt
        else:
            retx = 0
        if VERBOSE > 1:
            print("ret = %.2f" % retx)
        return retx

    def __str__(self):
        trarr = ""
        for cnt, aa in enumerate(self.trainarr):
            arr2 = rle(aa)
            res = str(self.resarr[cnt])
            if res == '\t':
                res = '\\t'
            trarr += "'" + res + "' " + \
                        str(arr2)[:70] + " ..\n"
            #if cnt > 20:
            #    break
        return trarr

    def dump(self):
        for cnt, aa in enumerate(self.trainarr):
            if VERBOSE > 2:
                print("%-2d" % cnt,  self.resarr[cnt], aa)
            else:
                arr2 = rle(aa)
                print("cnt: %-2d" % cnt, "'" + self.resarr[cnt] + "'", arr2)

    def showtrain(self):
        for aa in self.trainarr:
            print(aa)

# EOF
