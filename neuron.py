#!/usr/bin/env python

# ------------------------------------------------------------------------
# Neural network test

import random, math
import trans, tenticle, neuutil

#random.seed()

from neuutil import *

verbose = 0

# Help identify a neuron by serial number

gl_serial = 0

# ------------------------------------------------------------------------
# The basic building block
#

class neuron():

    def __init__(self, inputs, level, num):

        global gl_serial

        # These are helpers
        self.num = num; self.level = level
        self.serial = gl_serial; gl_serial += 1;

        if verbose:
            print("neuron init ", "%2d" % self.level, "%2d" % self.num, "    ", end=' ')

        # Tenticles are where the magic happens
        #self.tentarr = []
        #for aa in range(inputs):
        #    self.tentarr.append(tenticle.tenticle(self, aa, self.num))

        self.input  = neurand()
        self.weight = 0
        self.bias   = neurand() / 2

        # Output(s)
        self.output =  0. #tenticle.neurand()

    # --------------------------------------------------------------------
    # Fire one neuron.Call every tenticle's fire method and avarage it

    def fire(self):

        #sum = 0.; sum2 = 0xff; xlen = len(self.tentarr)
        #for aa in range(xlen):
        #    diff = self.tentarr[aa].fire(self)
        #    if aa % 2 == 0:
        #        sum += diff
        #    else:
        #        sum += diff
        #
        #    #print "%06x %06f - " % (sum2, diff),
        #    #sum2 ^= int(diff * 1000000)
        #
        #sum = float(sum2) / 1000000
        #sum += self.bias
        #sum /= len(self.tentarr)

        #self.output = sum
        #print "out: %+0.3f" % self.output,

        if 0: #pgdebug > 2:
            print("     Neuron:", self.level, self.num)
            for dd in self.tentarr:
                print(" [i=%0.3f" % dd.input, "w=%0.3f" % dd.weight, "b=%0.3f] " % dd.bias, end=' ')
                #print "[%0.3f]" % dd.input,
            print()
            print("     Out: %0.3f" % self.output)

        res =  (self.input +  self.bias) * self.weight
        self.output = trans.tfunc(res)
        #self.output = res


    def randtip(self, net, val):
        #neuutil.randmemb(self.tentarr).randtip(net, self, val)
        #if self.verbose:
        #    print("randtip", self.level, self.num, val)
        pass

    def show(self):
        return "i:%+.3f w:%+.3f b:%++.3f o:%+.3f" % \
            (self.input, self.weight, self.bias, self.output)

    def mutate(self, val):
        #print("mutate", val)
        #sum = 0.; sum2 = 0xff;
        #xlen = len(self.tentarr)
        self.weight += val
        #for aa in range(xlen):
        #    self.tentarr[aa].modify(val)

    def mutate2(self, val):
        #print("mutate", val)
        #sum = 0.; sum2 = 0xff;
        #xlen = len(self.tentarr)
        self.bias += val
        #for aa in range(xlen):
        #    self.tentarr[aa].modify(val)

    def diff(self, want):

        aa = want - self.output
        if aa > .1:
            return aa * 2

        return aa / 2

        #aa = sqr(want) - sqr(self.output)
        #if not aa:
        #    return 0
        #bb = math.sqrt(abs(aa))
        #if aa < 0: bb = -bb
        #return bb



if __name__ == '__main__':
    nn = neuron(1, 1, 0)
    #print("neuron", nn)
    #print("initial   ", nn.show())

    for aa in range(20):
        ddd = nn.diff(.5)
        print("d:", pn(ddd), end= " ")

        nn.mutate(ddd)

        #nn.mutate( neurand2() / 10 )
        #nn.mutate2( neurand2() / 10 )
        nn.fire()

        print(nn.show()) #, end = " | ")
        if 0: #aa % 2 == 1:
            print()

        if abs(ddd) < 0.001:
            break