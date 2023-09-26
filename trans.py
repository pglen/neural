#!/usr/bin/env python

import sys, math

# ------------------------------------------------------------------------
# Transfer function for neunet. Calculate logaritmic taper, preserve sign

from neuutil import *

# ------------------------------------------------------------------------
# The hyperbolic function

def tfunc(val):

    #print("tfunc", val)

    ret = 0.
    try:
        cc = float(val)
        ll = math.tanh(3* cc)
        ret =  ll
    except ValueError:
        print("Value error:", val, sys.exc_info())
        pass
    except:
        print(val, sys.exc_info())
        pass

    #if val < 0:
    #    ret = -ret;

    return ret

# ------------------------------------------------------------------------
# The traditional exponent

def tfunc2(val):
    ret = 0.
    try:
        cc = float(val)
        ll = math.log(1 + 30 * abs(cc))
        ret =  ll / 2
    except ValueError:
        print(val, sys.exc_info())
        pass
    except:
        print(val, sys.exc_info())
        pass
    if val < 0:
        ret = -ret;
    return ret

# ------------------------------------------------------------------------
# Do not use (testing)

def tfunc3(val):
    ret = 0.
    try:
        cc = float(val) * 5
        ll = 1. / (1. + math.exp(-cc))
        ret =  ll
    except ValueError:
        print(val, sys.exc_info())
        pass
    except:
        print("Exception", val, sys.exc_info())
        pass
    #if val < 0:
    #     ret = -ret;

    return ret


if __name__ == '__main__':

    #for aa in range(20):
    #    bb = -aa / 20
    #    print(pn(bb), pn(tfunc2(bb)), end=" | ")
    #    if aa % 4 == 3:
    #        print()
    #
    #print()
    #
    #for aa in range(20):
    #    bb = aa / 20
    #    print(pn(bb), pn(tfunc2(bb)), end=" | ")
    #    if aa % 4 == 3:
    #        print()

    xx = []; yy = []
    for aa in range(40):
        bb = aa / 20 - 1
        xx.append(bb)
        yy.append(tfunc(bb))


    import matplotlib.pyplot as plt


    plt.plot(xx, yy)
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.show()

