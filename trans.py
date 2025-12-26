#!/usr/bin/env python

import sys, math

# ------------------------------------------------------------------------
# Transfer function for neunet. Calculate logaritmic taper, preserve sign

#from neuutil import *

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

def generate(func):

    xx = []; yy = []
    for aa in range(80):
        bb = aa / 20 - 2
        xx.append(bb)
        yy.append(func(bb))
    return xx, yy

def draw(xx, yy):

    import matplotlib.pyplot as plt

    plt.plot(xx, yy)
    plt.xlabel("X values")
    plt.ylabel("Y values")
    plt.show()

def main():

    print("Generating ...")
    xx, yy = generate(tfunc)
    #xx, yy = generate(tfunc2)
    #xx, yy = generate(tfunc3)
    print("Drawing ...")
    draw(xx, yy)

if __name__ == '__main__':
    main()

# EOF
