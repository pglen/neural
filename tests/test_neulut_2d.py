#!/usr/bin/env python

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut

#neulut.VERBOSE = 0

VAL  = 1. ;  VAL2  = 0.51 ; OUT   = 1.

in_arr0 = ( \
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         )
in_arr1 = ( \
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         )
in_arr2 = ( \
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         )
in_arr3 = ( \
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         )
in_tarr0 = ( \
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         )
out_arr0 = [0, 0]
out_arr1 = [0, 1]
out_arr2 = [1, 0]
out_arr3 = [1, 1]

# ------------------------------------------------------------------------
# Tests

#if __name__ == '__main__':

def test_2d():

    ttt = time.time()
    nn = neulut.NeuLut(64, 2)
    nn.memorize(in_arr0, 8, out_arr0)
    nn.memorize(in_arr1, 8, out_arr1)
    nn.memorize(in_arr2, 8, out_arr2)
    nn.memorize(in_arr3, 8, out_arr3)

    aa = nn.recall(in_arr0, 1) ; aaa = nn.deviation
    bb = nn.recall(in_arr1, 1) ; bbb = nn.deviation
    cc = nn.recall(in_arr2, 1) ; ccc = nn.deviation
    dd = nn.recall(in_arr3, 1) ; ddd = nn.deviation
    ee = nn.recall(in_tarr0, 1); eee = nn.deviation
    print("exe time: %.2f us" % (1000000 *(time.time() - ttt)))

    print(aaa, aa)
    print(bbb, bb)
    print(ccc, cc)
    print(ddd, dd)
    print("tr:", eee, ee)  # Will match arr2 as configured

    assert ee == out_arr2

# EOF
