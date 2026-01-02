#!/usr/bin/env python

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut

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
        nn.recall(inarr, 1)
        print("%-5s" % kind, "in:", tin_arr[aa], "out:", nn.outputs,  end = " ")
        print("expect:", tout_arr[aa], end = " ")
        print(print_is_ok(nn.outputs,  tout_arr[aa]), "st:", nn.strength)

def tobits(val, lenx):
    ''' Convert number to digital bits '''
    arrx = []
    for aa in range(lenx-1, -1, -1):
        if val & 1 << aa: boolx = 1
        else: boolx = 0
        arrx.append(boolx)
    return arrx

VAL   = 1. ;  VAL2  = 0.51 ; OUT   = 1.
in_arr  =  ( (0, 0), (VAL, 0),  (0, VAL),  (VAL, VAL) )
tin_arr =  ( (0, 0), (VAL2, 0), (0, VAL2), (VAL2, VAL2) )
XOR, OR, AND, NAND, NOR = range(5)

if __name__ == '__main__':

    nn = neulut.NeuLut()

    # AND gate
    out_aarr =  (0, 0, 0, OUT)
    tout_aarr =  (0, 0, 0, VAL)
    train(AND, in_arr, out_aarr, nn)

    # OR gate
    out_oarr =  (0, OUT, OUT, OUT,)
    tout_oarr =  (0, VAL, VAL, VAL,)
    train(OR, in_arr, out_oarr, nn)

    # XOR gate
    out_xoarr =  (0, OUT, OUT, 0, )
    tout_xoarr =  (0, VAL, VAL, 0, )
    train(XOR, in_arr, out_xoarr, nn)

    # NAND gate
    out_narr =  (0, OUT, OUT, OUT, )
    tout_narr =  (0, VAL, VAL, VAL, )
    train(NAND, in_arr, out_narr, nn)

    # NOR gate
    out_norr =  (OUT, 0, 0, 0, )
    tout_norr =  (VAL, 0, 0, 0)
    train(NOR, in_arr, out_norr, nn)

    #print("Cummulative test:")
    testx("OR:", OR,  in_arr, out_oarr, tin_arr, tout_oarr, nn)
    testx("AND:", AND, in_arr, out_aarr, tin_arr, tout_aarr, nn)
    testx("XOR:", XOR, in_arr, out_xoarr, tin_arr, tout_xoarr, nn)
    testx("NAND:", NAND,in_arr, out_narr, tin_arr, tout_narr, nn)
    testx("NOR:",  NOR, in_arr, out_norr, tin_arr, tout_norr, nn)

# EOF
