#!/usr/bin/env python

''' Neural network test '''

import sys, random, math, array
from PIL import Image

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut
#neulut.VERBOSE = 2

from Crypto import Random
import secrets

class CustomArrayObject:
    def __init__(self, data_list):
        # Use Python's built-in array module for memory management
        self.data = array.array('B', data_list)
        self.shape = (len(data_list),)
        self.typestr = '|B' # '|d' for double (8-byte float)

    @property
    def __array_interface__(self):
        # Get the pointer to the underlying C data buffer
        data_ptr = self.data.buffer_info()[0]
        return {
            'shape': self.shape,
            'typestr': self.typestr,
            'data': (data_ptr, False), # Pointer and read-only flag (False for writeable)
            'version': 3 # Optional: interface version
        }


if __name__ == '__main__':

    sumx = Image.new("L", (800,602), color=(0) )
    pp = Image.new("L", (800,300), color=(20) )
    #pp2 = Image.new("L", (800,300), color=(30) )

    rrr = bytearray()
    for aa in range(300):
        for bb in range(800):
            rrr += bytearray((secrets.randbits(8),))
    #for aa in range(300):
    #    rrr += Random.get_random_bytes(800)
    pp = Image.frombytes("L", (800, 300), rrr)

    rrr = bytearray()
    for aa in range(300):
        rrr += Random.get_random_bytes(800)
    pp2 = Image.frombytes("L", (800, 300), rrr)

    #for aa in range(sumx.size[0]) :
    #    for bb in range(sumx.size[1]-1) :
    #        if bb < sumx.size[1] / 2:
    #            rrr = Random.get_random_bytes(3)
    #
    #            sumx.putpixel((aa, bb), rrr[2])
    #        else:
    #            rrr = secrets.randbits(8)
    #            sumx.putpixel((aa, bb + 1), rrr)


    sumx.paste(pp, (0, 0))
    sumx.paste(pp2, (0, 301))

    #print(dir())
    #secure_bits = secrets.randbits(8)
    #print(secure_bits)
    #sys.exit(0)
    sumx.show()

# EOF
